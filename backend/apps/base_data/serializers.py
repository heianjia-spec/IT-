import json
from rest_framework import serializers
from .models import AssetCategory, Department, Location, Supplier, AssetFormTemplate


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


class JsonField(serializers.CharField):
    """A CharField that accepts both JSON strings and Python dicts."""
    def to_internal_value(self, data):
        if isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        if isinstance(data, list):
            return json.dumps(data, ensure_ascii=False)
        return super().to_internal_value(data)

    def to_representation(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return {}
        return value or {}


class AssetFormTemplateSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    config = JsonField()

    class Meta:
        model = AssetFormTemplate
        fields = [
            'id', 'category', 'category_name', 'name',
            'config', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
