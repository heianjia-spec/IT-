from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from core.permissions import IsAdminOrAssetManager
from .models import AssetCategory, Department, Location, Supplier, AssetFormTemplate
from .serializers import (
    AssetCategorySerializer, AssetCategorySimpleSerializer,
    DepartmentSerializer, DepartmentSimpleSerializer,
    LocationSerializer, SupplierSerializer,
    AssetFormTemplateSerializer,
)
from .services import get_merged_template, get_inheritance_chain
from .field_registry import FIELD_REGISTRY


class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        if self.action == 'list':
            return AssetCategorySerializer
        return AssetCategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            return AssetCategory.objects.filter(parent__isnull=True)
        return AssetCategory.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    filterset_fields = ['is_active']
    search_fields = ['name', 'code']

    def get_serializer_class(self):
        return DepartmentSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Department.objects.filter(parent__isnull=True)
        return Department.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ['is_active', 'location_type']
    search_fields = ['name', 'code']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'contact_person']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []


class AssetFormTemplateViewSet(viewsets.ModelViewSet):
    queryset = AssetFormTemplate.objects.select_related('category').all()
    serializer_class = AssetFormTemplateSerializer
    filterset_fields = ['is_active']
    search_fields = ['name', 'category__name']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrAssetManager()]
        return []

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get merged form template for a given category (with tree inheritance)."""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id is required'}, status=400)
        try:
            category = AssetCategory.objects.get(id=category_id, is_active=True)
        except AssetCategory.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

        merged = get_merged_template(category)
        chain = get_inheritance_chain(category)
        return Response({
            'category_id': category.id,
            'category_name': category.name,
            'template': merged,
            'inheritance_chain': chain,
        })

    @action(detail=False, methods=['get'])
    def field_registry(self, request):
        """Return all available field definitions for template editor."""
        return Response({'fields': list(FIELD_REGISTRY.values())})
