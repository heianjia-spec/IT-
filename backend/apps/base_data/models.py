from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class AssetCategory(MPTTModel):
    """Asset category tree, e.g. 硬件 > 服务器, 硬件 > 网络设备 > 交换机"""
    name = models.CharField('分类名称', max_length=100)
    code = models.CharField('分类编码', max_length=50, unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children',
        verbose_name='上级分类'
    )
    description = models.TextField('描述', blank=True, default='')
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    class Meta:
        db_table = 'base_asset_category'
        verbose_name = '资产分类'
        verbose_name_plural = '资产分类'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(MPTTModel):
    """Department tree, e.g. 技术部 > 运维组"""
    name = models.CharField('部门名称', max_length=100)
    code = models.CharField('部门编码', max_length=50, unique=True)
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name='children',
        verbose_name='上级部门'
    )
    manager = models.CharField('负责人', max_length=50, blank=True, default='')
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['sort_order']

    class Meta:
        db_table = 'base_department'
        verbose_name = '部门'
        verbose_name_plural = '部门'

    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(models.Model):
    """Storage location"""
    LOCATION_TYPE_CHOICES = [
        ('server_room', '机房'),
        ('warehouse', '库房'),
        ('office', '办公室'),
        ('other', '其他'),
    ]
    name = models.CharField('位置名称', max_length=100)
    code = models.CharField('位置编码', max_length=50, unique=True)
    location_type = models.CharField('位置类型', max_length=20, choices=LOCATION_TYPE_CHOICES, default='warehouse')
    address = models.TextField('详细地址', blank=True, default='')
    description = models.TextField('描述', blank=True, default='')
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'base_location'
        verbose_name = '位置'
        verbose_name_plural = '位置'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Supplier(models.Model):
    """Supplier/vendor"""
    name = models.CharField('供应商名称', max_length=100)
    code = models.CharField('供应商编码', max_length=50, unique=True)
    contact_person = models.CharField('联系人', max_length=50, blank=True, default='')
    contact_phone = models.CharField('联系电话', max_length=30, blank=True, default='')
    address = models.TextField('地址', blank=True, default='')
    description = models.TextField('描述', blank=True, default='')
    is_active = models.BooleanField('启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'base_supplier'
        verbose_name = '供应商'
        verbose_name_plural = '供应商'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"
