from datetime import date
from django.db import models
from django.conf import settings


class Asset(models.Model):
    """Unified asset model for all asset types."""

    ASSET_TYPE_CHOICES = [
        ('server', '服务器'),
        ('pc', 'PC'),
        ('printer', '打印机'),
        ('network_device', '网络设备'),
        ('switch', '交换机'),
        ('multimedia', '多媒体设备'),
        ('software', '软件'),
        ('consumable', '耗材'),
    ]

    STATUS_CHOICES = [
        ('in_stock', '在库'),
        ('in_use', '在用'),
        ('borrowed', '借用'),
        ('repair', '维修'),
        ('scrapped', '报废'),
        ('transferring', '调拨中'),
    ]

    # ========== Basic Info ==========
    asset_number = models.CharField('资产编号', max_length=50, unique=True, db_index=True, blank=True, default='')
    name = models.CharField('资产名称', max_length=200, blank=True, default='')
    asset_type = models.CharField('资产类型', max_length=20, choices=ASSET_TYPE_CHOICES, db_index=True)
    category = models.ForeignKey(
        'base_data.AssetCategory',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='assets',
        verbose_name='资产分类'
    )
    brand = models.CharField('品牌', max_length=100, blank=True, default='')
    spec_model = models.CharField('规格型号', max_length=200, blank=True, default='')
    serial_number = models.CharField('序列号/SN码', max_length=200, blank=True, default='')
    nc_number = models.CharField('NC编号', max_length=50, blank=True, default='')
    status = models.CharField(
        '资产状态', max_length=20,
        choices=STATUS_CHOICES, default='in_stock', db_index=True
    )
    department = models.ForeignKey(
        'base_data.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assets',
        verbose_name='使用部门'
    )
    responsible_person = models.CharField('责任人', max_length=50, blank=True, default='')
    location = models.ForeignKey(
        'base_data.Location',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assets',
        verbose_name='存放位置'
    )
    room_name = models.CharField('机房名称', max_length=100, blank=True, default='')
    cabinet_no = models.CharField('机柜编号', max_length=50, blank=True, default='')
    storage_location = models.CharField('存放位置描述', max_length=200, blank=True, default='')
    remarks = models.TextField('备注', blank=True, default='')

    # ========== Purchase Info ==========
    purchase_date = models.DateField('购置日期', null=True, blank=True)
    production_date = models.DateField('生产日期', null=True, blank=True)
    purchase_amount = models.DecimalField('购置金额(元)', max_digits=12, decimal_places=2, null=True, blank=True)
    depreciation_years = models.IntegerField('折旧年限', null=True, blank=True)
    supplier = models.ForeignKey(
        'base_data.Supplier',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assets',
        verbose_name='供应商'
    )
    warranty_expiry = models.DateField('保修截止日期', null=True, blank=True)
    WARRANTY_STATUS_CHOICES = [
        ('under_warranty', '在保'),
        ('expired', '过保'),
    ]
    warranty_status = models.CharField(
        '保修状态', max_length=20,
        choices=WARRANTY_STATUS_CHOICES,
        blank=True, default=''
    )

    # ========== Hardware Fields ==========
    cpu_model = models.CharField('CPU型号', max_length=200, blank=True, default='')
    memory_info = models.CharField('内存', max_length=100, blank=True, default='')
    disk_size = models.CharField('硬盘', max_length=200, blank=True, default='')
    os = models.CharField('操作系统', max_length=100, blank=True, default='')
    has_monitor = models.BooleanField('是否带显示器', null=True, blank=True)
    monitor_model = models.CharField('显示器型号', max_length=200, blank=True, default='')
    oob_address = models.CharField('管理地址(OOB)', max_length=100, blank=True, default='')
    nic_info = models.TextField('网卡信息', blank=True, default='')
    ip_address = models.CharField('IP地址/管理地址', max_length=100, blank=True, default='')
    mac_address = models.CharField('MAC地址', max_length=50, blank=True, default='')
    port_count = models.IntegerField('端口数量', null=True, blank=True)
    firmware = models.CharField('固件版本', max_length=100, blank=True, default='')

    # ========== Printer-specific ==========
    PRINTER_TYPE_CHOICES = [
        ('laser', '激光'), ('inkjet', '喷墨'),
        ('dot_matrix', '针式'), ('mfp', '多功能一体机'),
    ]
    printer_type = models.CharField('打印机类型', max_length=20, choices=PRINTER_TYPE_CHOICES, blank=True, default='')
    is_color = models.BooleanField('是否彩色', null=True, blank=True)
    is_duplex = models.BooleanField('是否双面打印', null=True, blank=True)
    CONNECT_TYPE_CHOICES = [
        ('usb', 'USB'), ('wired', '有线网络'), ('wifi', 'WiFi'),
    ]
    connect_type = models.CharField('连接方式', max_length=20, choices=CONNECT_TYPE_CHOICES, blank=True, default='')
    cartridge_model = models.CharField('硒鼓/墨盒型号', max_length=200, blank=True, default='')

    # ========== Network-device-specific ==========
    NETWORK_TYPE_CHOICES = [
        ('router', '路由器'), ('firewall', '防火墙'),
        ('switch_dev', '交换机'), ('load_balancer', '负载均衡'),
        ('wireless_controller', '无线控制器'), ('vpn_gateway', 'VPN网关'),
    ]
    network_type = models.CharField('网络设备类型', max_length=30, choices=NETWORK_TYPE_CHOICES, blank=True, default='')
    port_type = models.CharField('端口类型', max_length=100, blank=True, default='')
    poe_support = models.BooleanField('是否支持PoE', null=True, blank=True)
    poe_power = models.IntegerField('PoE功率(W)', null=True, blank=True)
    stackable = models.BooleanField('是否可堆叠', null=True, blank=True)
    stack_id = models.CharField('堆叠编号', max_length=50, blank=True, default='')
    redundancy_power = models.BooleanField('是否冗余电源', null=True, blank=True)
    rack_position = models.CharField('机架位置', max_length=100, blank=True, default='')

    # ========== Software-specific ==========
    SOFTWARE_TYPE_CHOICES = [
        ('os', '操作系统'), ('office', '办公软件'), ('database', '数据库'),
        ('middleware', '中间件'), ('security', '安全软件'), ('design', '设计软件'),
        ('business', '业务应用'), ('dev_tool', '开发工具'), ('other', '其他'),
    ]
    software_type = models.CharField('软件类型', max_length=20, choices=SOFTWARE_TYPE_CHOICES, blank=True, default='')
    version = models.CharField('版本号', max_length=50, blank=True, default='')
    LICENSE_TYPE_CHOICES = [
        ('perpetual', '永久授权'), ('subscription', '订阅制'),
        ('opensource', '开源'), ('self_developed', '自研'),
    ]
    license_type = models.CharField('授权类型', max_length=20, choices=LICENSE_TYPE_CHOICES, blank=True, default='')
    license_key = models.CharField('许可证号', max_length=200, blank=True, default='')
    license_count = models.IntegerField('授权数量', null=True, blank=True)
    used_count = models.IntegerField('已用数量', null=True, blank=True)
    license_expiry = models.DateField('许可到期日期', null=True, blank=True)
    platform = models.CharField('运行平台', max_length=100, blank=True, default='')
    installed_device = models.TextField('安装设备', blank=True, default='')

    # ========== Consumable-specific ==========
    CONSUMABLE_TYPE_CHOICES = [
        ('toner', '硒鼓'), ('cartridge', '墨盒'), ('paper', '打印纸'),
        ('cable', '网线'), ('fiber', '光纤跳线'), ('keyboard_mouse', '键盘鼠标'),
        ('disc', '光盘'), ('cable_other', '线缆'), ('other', '其他'),
    ]
    consumable_type = models.CharField('耗材类型', max_length=20, choices=CONSUMABLE_TYPE_CHOICES, blank=True, default='')
    UNIT_CHOICES = [
        ('piece', '个'), ('box', '箱'), ('pack', '包'), ('roll', '卷'), ('carton', '盒'),
    ]
    unit = models.CharField('单位', max_length=10, choices=UNIT_CHOICES, blank=True, default='')
    current_stock = models.IntegerField('当前库存', null=True, blank=True)
    min_stock = models.IntegerField('最低库存预警', null=True, blank=True)
    applicable_device = models.TextField('适用设备', blank=True, default='')
    unit_price = models.DecimalField('单价', max_digits=10, decimal_places=2, null=True, blank=True)
    last_purchase_date = models.DateField('上次采购日期', null=True, blank=True)

    # ========== Audit ==========
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_assets',
        verbose_name='创建人'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'asset_asset'
        verbose_name = '资产'
        verbose_name_plural = '资产'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset_type', 'status']),
            models.Index(fields=['department']),
            models.Index(fields=['warranty_expiry']),
        ]

    def __str__(self):
        return f"[{self.asset_number}] {self.name or self.get_asset_type_display()}"

    def _derive_asset_type(self):
        """Auto-set asset_type from category tree."""
        if not self.category:
            return
        # Get root ancestor of the category
        root = self.category.get_root()
        root_name = root.name
        cat_name = self.category.name

        if root_name == '硬件':
            # Map subcategory names to asset_type
            hw_map = {
                '服务器': 'server', 'PC': 'pc', '打印机': 'printer',
                '网络设备': 'network_device', '路由器': 'network_device',
                '交换机': 'switch', '防火墙': 'network_device',
                '无线控制器': 'network_device',
            }
            self.asset_type = hw_map.get(cat_name, 'server')
        elif root_name == '软件':
            self.asset_type = 'software'
        elif root_name == 'IT耗材':
            self.asset_type = 'consumable'
        elif root_name == '多媒体':
            self.asset_type = 'multimedia'

    def save(self, *args, **kwargs):
        if self.warranty_expiry:
            self.warranty_status = 'expired' if self.warranty_expiry < date.today() else 'under_warranty'
        else:
            self.warranty_status = ''
        self._derive_asset_type()
        if not self.asset_number:
            today = date.today()
            prefix = f"IT-{today.strftime('%Y%m%d')}-"
            last = Asset.objects.filter(
                asset_number__startswith=prefix
            ).order_by('-asset_number').first()
            seq = int(last.asset_number[-4:]) + 1 if last else 1
            self.asset_number = f"{prefix}{seq:04d}"
        super().save(*args, **kwargs)


class AssetStatusChange(models.Model):
    """Audit log for asset status changes."""
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE,
        related_name='status_changes',
        verbose_name='资产'
    )
    from_status = models.CharField('变更前状态', max_length=20, blank=True, default='')
    to_status = models.CharField('变更后状态', max_length=20)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='status_changes',
        verbose_name='操作人'
    )
    remarks = models.TextField('备注', blank=True, default='')
    created_at = models.DateTimeField('操作时间', auto_now_add=True)

    class Meta:
        db_table = 'asset_status_change'
        verbose_name = '状态变更记录'
        verbose_name_plural = '状态变更记录'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.asset.asset_number}: {self.from_status} → {self.to_status}"


class OperationLog(models.Model):
    """Audit log for asset create/delete/import/export operations."""
    ACTION_CHOICES = [
        ('create', '新增资产'),
        ('update', '编辑资产'),
        ('delete', '删除资产'),
        ('batch_delete', '批量删除'),
        ('import', '导入资产'),
        ('export', '导出资产'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='operation_logs',
        verbose_name='操作人'
    )
    action_type = models.CharField('操作类型', max_length=20, choices=ACTION_CHOICES, db_index=True)
    asset = models.ForeignKey(
        Asset, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='operation_logs',
        verbose_name='关联资产'
    )
    asset_count = models.IntegerField('资产数量', default=0)
    detail = models.TextField('操作详情', blank=True, default='')
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)
    created_at = models.DateTimeField('操作时间', auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'asset_operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_action_type_display()}] {self.user or '-'} — {self.created_at}"
