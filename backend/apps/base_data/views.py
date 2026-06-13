from rest_framework import viewsets
from core.permissions import IsAdminOrAssetManager
from .models import AssetCategory, Department, Location, Supplier
from .serializers import (
    AssetCategorySerializer, AssetCategorySimpleSerializer,
    DepartmentSerializer, DepartmentSimpleSerializer,
    LocationSerializer, SupplierSerializer
)


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
