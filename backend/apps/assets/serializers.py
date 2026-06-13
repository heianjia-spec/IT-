from rest_framework import serializers
from .models import Asset, AssetStatusChange, OperationLog


class AssetListSerializer(serializers.ModelSerializer):
    """Compact serializer for list view."""
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)

    class Meta:
        model = Asset
        fields = [
            'id', 'asset_number', 'name', 'asset_type', 'asset_type_display',
            'category', 'category_name', 'brand', 'spec_model', 'serial_number',
            'status', 'status_display', 'department', 'department_name',
            'responsible_person', 'warranty_expiry', 'warranty_status',
            'created_at', 'updated_at',
        ]


class AssetSerializer(serializers.ModelSerializer):
    """Full serializer for detail/create/update."""
    asset_number = serializers.CharField(
        required=False, allow_blank=True, default='', max_length=50
    )
    asset_type = serializers.CharField(required=False, allow_blank=True, default='', max_length=20)
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    department_name = serializers.CharField(source='department.name', read_only=True, default=None)
    location_name = serializers.CharField(source='location.name', read_only=True, default=None)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, default=None)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, default=None)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'warranty_status']


class OperationLogSerializer(serializers.ModelSerializer):
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True, default=None)

    class Meta:
        model = OperationLog
        fields = [
            'id', 'user', 'user_name', 'action_type', 'action_type_display',
            'asset', 'asset_count', 'detail', 'ip_address', 'created_at',
        ]
        read_only_fields = fields


class AssetStatusChangeSerializer(serializers.ModelSerializer):
    from_status_display = serializers.SerializerMethodField()
    to_status_display = serializers.SerializerMethodField()
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True, default=None)

    class Meta:
        model = AssetStatusChange
        fields = [
            'id', 'asset', 'from_status', 'from_status_display',
            'to_status', 'to_status_display',
            'changed_by', 'changed_by_name', 'remarks', 'created_at'
        ]

    def get_from_status_display(self, obj):
        return dict(Asset.STATUS_CHOICES).get(obj.from_status, obj.from_status)

    def get_to_status_display(self, obj):
        return dict(Asset.STATUS_CHOICES).get(obj.to_status, obj.to_status)
