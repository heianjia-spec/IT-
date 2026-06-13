from rest_framework import serializers
from .models import AssetCategory, Department, Location, Supplier


class AssetCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_code = serializers.CharField(source='parent.code', read_only=True, default=None)

    class Meta:
        model = AssetCategory
        fields = [
            'id', 'name', 'code', 'parent', 'parent_code',
            'description', 'sort_order', 'is_active', 'created_at', 'children'
        ]
        read_only_fields = ['id', 'created_at']

    def get_children(self, obj):
        children = obj.get_children()
        if children.exists():
            return AssetCategorySerializer(children, many=True, context=self.context).data
        return []


class AssetCategorySimpleSerializer(serializers.ModelSerializer):
    """Flat serializer without children — for dropdown options."""
    class Meta:
        model = AssetCategory
        fields = ['id', 'name', 'code']


class DepartmentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_code = serializers.CharField(source='parent.code', read_only=True, default=None)

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'code', 'parent', 'parent_code',
            'manager', 'sort_order', 'is_active', 'created_at', 'children'
        ]
        read_only_fields = ['id', 'created_at']

    def get_children(self, obj):
        children = obj.get_children()
        if children.exists():
            return DepartmentSerializer(children, many=True, context=self.context).data
        return []


class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code']


class LocationSerializer(serializers.ModelSerializer):
    location_type_display = serializers.CharField(source='get_location_type_display', read_only=True)

    class Meta:
        model = Location
        fields = [
            'id', 'name', 'code', 'location_type', 'location_type_display',
            'address', 'description', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'code', 'contact_person', 'contact_phone',
            'address', 'description', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
