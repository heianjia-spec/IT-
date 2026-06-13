from datetime import date, timedelta
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from assets.models import Asset


class DashboardViewSet(viewsets.ViewSet):
    """Dashboard statistics API."""

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Asset count summary."""
        qs = Asset.objects.all()
        total = qs.count()
        in_use = qs.filter(status='in_use').count()
        in_stock = qs.filter(status='in_stock').count()
        scrapped = qs.filter(status='scrapped').count()
        borrowed = qs.filter(status='borrowed').count()
        repair = qs.filter(status='repair').count()
        transferring = qs.filter(status='transferring').count()

        return Response({
            'total': total,
            'in_use': in_use,
            'in_stock': in_stock,
            'scrapped': scrapped,
            'borrowed': borrowed,
            'repair': repair,
            'transferring': transferring,
        })

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Asset count grouped by asset type."""
        data = Asset.objects.values('asset_type').annotate(
            count=Count('id')
        ).order_by('-count')
        type_map = dict(Asset.ASSET_TYPE_CHOICES)
        result = []
        for item in data:
            result.append({
                'asset_type': item['asset_type'],
                'type_display': type_map.get(item['asset_type'], item['asset_type']),
                'count': item['count'],
            })
        return Response(result)

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Asset count grouped by department."""
        data = Asset.objects.values('department__name').annotate(
            count=Count('id')
        ).exclude(department__isnull=True).order_by('-count')
        return Response(list(data))

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Asset count grouped by status, optionally filtered by asset_type."""
        qs = Asset.objects.all()
        asset_type = request.query_params.get('asset_type', '')
        if asset_type:
            qs = qs.filter(asset_type=asset_type)
        data = qs.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        status_map = dict(Asset.STATUS_CHOICES)
        result = []
        for item in data:
            result.append({
                'status': item['status'],
                'status_display': status_map.get(item['status'], item['status']),
                'count': item['count'],
            })
        return Response(result)

    @action(detail=False, methods=['get'])
    def expiry_reminders(self, request):
        """Upcoming warranty/license expirations."""
        today = date.today()
        deadline = today + timedelta(days=90)
        warranty_expiring = Asset.objects.filter(
            Q(warranty_expiry__gte=today) & Q(warranty_expiry__lte=deadline)
        ).values('id', 'asset_number', 'name', 'warranty_expiry')[:50]

        license_expiring = Asset.objects.filter(
            Q(license_expiry__gte=today) & Q(license_expiry__lte=deadline)
        ).values('id', 'asset_number', 'name', 'license_expiry')[:50]

        return Response({
            'warranty_expiring': list(warranty_expiring),
            'license_expiring': list(license_expiring),
        })
