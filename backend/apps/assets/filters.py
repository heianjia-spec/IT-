import django_filters
from .models import Asset


class AssetFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='关键字搜索')
    status = django_filters.ChoiceFilter(choices=Asset.STATUS_CHOICES)
    asset_type = django_filters.ChoiceFilter(choices=Asset.ASSET_TYPE_CHOICES)
    department = django_filters.NumberFilter(field_name='department_id')
    category = django_filters.NumberFilter(method='filter_category')
    purchase_date_from = django_filters.DateFilter(field_name='purchase_date', lookup_expr='gte')
    purchase_date_to = django_filters.DateFilter(field_name='purchase_date', lookup_expr='lte')
    warranty_status = django_filters.ChoiceFilter(choices=Asset.WARRANTY_STATUS_CHOICES)

    class Meta:
        model = Asset
        fields = ['status', 'asset_type', 'department', 'category', 'warranty_status']

    def filter_category(self, queryset, name, value):
        """Filter by category including all descendants."""
        from base_data.models import AssetCategory
        try:
            category = AssetCategory.objects.get(pk=value)
            ids = category.get_descendants(include_self=True).values_list('id', flat=True)
            return queryset.filter(category_id__in=ids)
        except AssetCategory.DoesNotExist:
            return queryset.none()

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(asset_number__icontains=value) |
            models.Q(name__icontains=value) |
            models.Q(serial_number__icontains=value) |
            models.Q(nc_number__icontains=value) |
            models.Q(responsible_person__icontains=value)
        )


# Need to import models for Q
from django.db import models
