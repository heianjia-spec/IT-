from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.http import HttpResponse
from core.permissions import IsAdminOrAssetManager
from .models import Asset, AssetStatusChange, OperationLog
from .serializers import AssetListSerializer, AssetSerializer, AssetStatusChangeSerializer, OperationLogSerializer
from .filters import AssetFilter
from .import_export import generate_import_template, import_assets_from_excel, export_assets_to_excel
from .qrcode_utils import generate_asset_qrcode


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.select_related(
        'category', 'department', 'location', 'supplier', 'created_by'
    ).all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AssetFilter
    search_fields = ['asset_number', 'name', 'serial_number', 'nc_number']
    ordering_fields = ['created_at', 'asset_number', 'name', 'purchase_date', 'purchase_amount']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return AssetListSerializer
        return AssetSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy',
                           'import_assets'):
            return [IsAdminOrAssetManager()]
        return []

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        OperationLog.objects.create(
            user=self.request.user,
            action_type='create',
            asset=instance,
            asset_count=1,
            detail=f'新增资产：{instance.name or instance.asset_number}',
            ip_address=get_client_ip(self.request),
        )

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        new_status = instance.status
        if old_status != new_status:
            AssetStatusChange.objects.create(
                asset=instance,
                from_status=old_status,
                to_status=new_status,
                changed_by=self.request.user,
                remarks=f'状态由 {dict(Asset.STATUS_CHOICES).get(old_status, old_status)} 变更为 {dict(Asset.STATUS_CHOICES).get(new_status, new_status)}'
            )

    def perform_destroy(self, instance):
        OperationLog.objects.create(
            user=self.request.user,
            action_type='delete',
            asset=instance,
            asset_count=1,
            detail=f'删除资产：{instance.name or instance.asset_number}',
            ip_address=get_client_ip(self.request),
        )
        instance.delete()

    @action(detail=False, methods=['post'])
    def batch_delete(self, request):
        """Batch delete assets by IDs."""
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': '请提供要删除的资产ID列表'}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = Asset.objects.filter(id__in=ids).delete()
        OperationLog.objects.create(
            user=request.user,
            action_type='batch_delete',
            asset_count=deleted,
            detail=f'批量删除资产：{deleted} 条 (IDs: {ids})',
            ip_address=get_client_ip(request),
        )
        return Response({'deleted': deleted, 'message': f'成功删除 {deleted} 条资产'})

    @action(detail=True, methods=['get'])
    def status_history(self, request, pk=None):
        asset = self.get_object()
        changes = asset.status_changes.select_related('changed_by').all()
        serializer = AssetStatusChangeSerializer(changes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def template(self, request):
        """Download import template."""
        asset_type = request.query_params.get('asset_type', '')
        output = generate_import_template(asset_type)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=asset_import_template.xlsx'
        return response

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser])
    def import_assets(self, request):
        """Import assets from uploaded Excel file."""
        file = request.FILES.get('file')
        asset_type = request.data.get('asset_type', '')
        if not file:
            return Response({'error': '请上传文件'}, status=status.HTTP_400_BAD_REQUEST)
        if not file.name.endswith('.xlsx'):
            return Response({'error': '请上传 .xlsx 格式文件'}, status=status.HTTP_400_BAD_REQUEST)

        success_list, error_list = import_assets_from_excel(file, asset_type)
        OperationLog.objects.create(
            user=request.user,
            action_type='import',
            asset_count=len(success_list),
            detail=f'导入资产：成功 {len(success_list)} 条，失败 {len(error_list)} 条',
            ip_address=get_client_ip(request),
        )
        return Response({
            'success_count': len(success_list),
            'error_count': len(error_list),
            'errors': error_list,
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export assets to Excel."""
        queryset = self.filter_queryset(self.get_queryset())
        fields_param = request.query_params.get('fields', '')
        fields = fields_param.split(',') if fields_param else None
        count = queryset.count()
        OperationLog.objects.create(
            user=request.user,
            action_type='export',
            asset_count=count,
            detail=f'导出资产：{count} 条',
            ip_address=get_client_ip(request),
        )
        output = export_assets_to_excel(queryset, fields)
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=asset_export.xlsx'
        return response

    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        """Generate QR code for an asset."""
        asset = self.get_object()
        buf = generate_asset_qrcode(asset)
        return HttpResponse(buf.getvalue(), content_type='image/png')


class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only operation log viewer."""
    queryset = OperationLog.objects.select_related('user', 'asset').all()
    serializer_class = OperationLogSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['action_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
