"""
Initialize form templates for asset categories.
Creates templates with tree inheritance:
  - 硬件 (root) → common hardware fields
  - 打印机 → inherits hardware + adds printer-specific
  - 网络设备 → inherits hardware + adds network-specific
  - 交换机 → inherits network-device + adds switch-specific
  - 软件 (root) → software-specific fields
  - IT耗材 (root) → consumable-specific fields
Idempotent — safe to run multiple times.
"""
import json
from django.core.management.base import BaseCommand
from base_data.models import AssetCategory, AssetFormTemplate


def make_config(sections):
    """Serialize config dict to JSON string for TextField storage."""
    return json.dumps({'sections': sections}, ensure_ascii=False)


class Command(BaseCommand):
    help = 'Initialize form template seed data (idempotent)'

    def handle(self, *args, **options):
        self._create_templates()
        self.stdout.write(self.style.SUCCESS('Form templates initialized.'))

    @staticmethod
    def _create_templates():
        if AssetFormTemplate.objects.exists():
            return

        categories = {c.code: c for c in AssetCategory.objects.all()}

        # ============================
        # 1. 硬件 (root) — common hardware fields
        # ============================
        hardware = categories.get('hardware')
        if hardware:
            AssetFormTemplate.objects.create(
                category=hardware,
                name='硬件默认模板',
                config=make_config([
                    {
                        'name': '硬件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'cpu_model', 'label': 'CPU型号', 'widget': 'text', 'required': False, 'sort_order': 1, 'span': 8},
                            {'key': 'memory_info', 'label': '内存', 'widget': 'text', 'required': False, 'sort_order': 2, 'span': 8},
                            {'key': 'disk_size', 'label': '硬盘', 'widget': 'text', 'required': False, 'sort_order': 3, 'span': 8},
                            {'key': 'os', 'label': '操作系统', 'widget': 'text', 'required': False, 'sort_order': 4, 'span': 8},
                            {'key': 'ip_address', 'label': 'IP地址/管理地址', 'widget': 'text', 'required': False, 'sort_order': 5, 'span': 8},
                            {'key': 'mac_address', 'label': 'MAC地址', 'widget': 'text', 'required': False, 'sort_order': 6, 'span': 8},
                            {'key': 'oob_address', 'label': '管理地址(OOB)', 'widget': 'text', 'required': False, 'sort_order': 7, 'span': 8},
                            {'key': 'nic_info', 'label': '网卡信息', 'widget': 'textarea', 'required': False, 'sort_order': 8, 'span': 24},
                            {'key': 'port_count', 'label': '端口数量', 'widget': 'number', 'required': False, 'sort_order': 9, 'span': 8},
                            {'key': 'firmware', 'label': '固件版本', 'widget': 'text', 'required': False, 'sort_order': 10, 'span': 8},
                            {'key': 'redundancy_power', 'label': '是否冗余电源', 'widget': 'switch', 'required': False, 'sort_order': 11, 'span': 8},
                            {'key': 'rack_position', 'label': '机架位置', 'widget': 'text', 'required': False, 'sort_order': 12, 'span': 8},
                        ],
                    },
                ]),
            )

        # ============================
        # 2. PC — inherits hardware + adds monitor fields
        # ============================
        pc = categories.get('hw_pc')
        if pc:
            AssetFormTemplate.objects.create(
                category=pc,
                name='PC模板',
                config=make_config([
                    {
                        'name': '硬件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'has_monitor', 'label': '是否带显示器', 'widget': 'switch', 'required': False, 'sort_order': 20, 'span': 8},
                            {'key': 'monitor_model', 'label': '显示器型号', 'widget': 'text', 'required': False, 'sort_order': 21, 'span': 8},
                        ],
                    },
                ]),
            )

        # ============================
        # 3. 打印机 — inherits hardware + adds printer-specific
        # ============================
        printer_cat = categories.get('hw_printer')
        if printer_cat:
            AssetFormTemplate.objects.create(
                category=printer_cat,
                name='打印机模板',
                config=make_config([
                    {
                        'name': '硬件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'printer_type', 'label': '打印机类型', 'widget': 'select', 'required': False, 'sort_order': 20, 'span': 8,
                             'options': [{'value': 'laser', 'label': '激光'}, {'value': 'inkjet', 'label': '喷墨'}, {'value': 'dot_matrix', 'label': '针式'}, {'value': 'mfp', 'label': '多功能一体机'}]},
                            {'key': 'is_color', 'label': '是否彩色', 'widget': 'switch', 'required': False, 'sort_order': 21, 'span': 8},
                            {'key': 'is_duplex', 'label': '是否双面打印', 'widget': 'switch', 'required': False, 'sort_order': 22, 'span': 8},
                            {'key': 'connect_type', 'label': '连接方式', 'widget': 'select', 'required': False, 'sort_order': 23, 'span': 8,
                             'options': [{'value': 'usb', 'label': 'USB'}, {'value': 'wired', 'label': '有线网络'}, {'value': 'wifi', 'label': 'WiFi'}]},
                            {'key': 'cartridge_model', 'label': '硒鼓/墨盒型号', 'widget': 'text', 'required': False, 'sort_order': 24, 'span': 8},
                        ],
                    },
                ]),
            )

        # ============================
        # 4. 网络设备 — inherits hardware + adds network-specific
        # ============================
        network = categories.get('hw_network')
        if network:
            AssetFormTemplate.objects.create(
                category=network,
                name='网络设备模板',
                config=make_config([
                    {
                        'name': '硬件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'network_type', 'label': '网络设备类型', 'widget': 'select', 'required': False, 'sort_order': 20, 'span': 8,
                             'options': [{'value': 'router', 'label': '路由器'}, {'value': 'firewall', 'label': '防火墙'}, {'value': 'switch_dev', 'label': '交换机'}, {'value': 'load_balancer', 'label': '负载均衡'}, {'value': 'wireless_controller', 'label': '无线控制器'}, {'value': 'vpn_gateway', 'label': 'VPN网关'}]},
                            {'key': 'port_type', 'label': '端口类型', 'widget': 'text', 'required': False, 'sort_order': 21, 'span': 8},
                            {'key': 'poe_support', 'label': '是否支持PoE', 'widget': 'switch', 'required': False, 'sort_order': 22, 'span': 8},
                            {'key': 'poe_power', 'label': 'PoE功率(W)', 'widget': 'number', 'required': False, 'sort_order': 23, 'span': 8},
                        ],
                    },
                ]),
            )

        # ============================
        # 5. 交换机 — inherits network-device + adds switch-specific
        # ============================
        switch_cat = categories.get('hw_switch')
        if switch_cat:
            AssetFormTemplate.objects.create(
                category=switch_cat,
                name='交换机模板',
                config=make_config([
                    {
                        'name': '硬件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'stackable', 'label': '是否可堆叠', 'widget': 'switch', 'required': False, 'sort_order': 30, 'span': 8},
                            {'key': 'stack_id', 'label': '堆叠编号', 'widget': 'text', 'required': False, 'sort_order': 31, 'span': 8},
                        ],
                    },
                ]),
            )

        # ============================
        # 6. 软件 (root) — software-specific fields
        # ============================
        software = categories.get('software')
        if software:
            AssetFormTemplate.objects.create(
                category=software,
                name='软件默认模板',
                config=make_config([
                    {
                        'name': '软件信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'software_type', 'label': '软件类型', 'widget': 'select', 'required': False, 'sort_order': 1, 'span': 8,
                             'options': [{'value': 'os', 'label': '操作系统'}, {'value': 'office', 'label': '办公软件'}, {'value': 'database', 'label': '数据库'}, {'value': 'middleware', 'label': '中间件'}, {'value': 'security', 'label': '安全软件'}, {'value': 'design', 'label': '设计软件'}, {'value': 'business', 'label': '业务应用'}, {'value': 'dev_tool', 'label': '开发工具'}, {'value': 'other', 'label': '其他'}]},
                            {'key': 'version', 'label': '版本号', 'widget': 'text', 'required': False, 'sort_order': 2, 'span': 8},
                            {'key': 'license_type', 'label': '授权类型', 'widget': 'select', 'required': False, 'sort_order': 3, 'span': 8,
                             'options': [{'value': 'perpetual', 'label': '永久授权'}, {'value': 'subscription', 'label': '订阅制'}, {'value': 'opensource', 'label': '开源'}, {'value': 'self_developed', 'label': '自研'}]},
                            {'key': 'license_key', 'label': '许可证号', 'widget': 'text', 'required': False, 'sort_order': 4, 'span': 8},
                            {'key': 'license_count', 'label': '授权数量', 'widget': 'number', 'required': False, 'sort_order': 5, 'span': 8},
                            {'key': 'used_count', 'label': '已用数量', 'widget': 'number', 'required': False, 'sort_order': 6, 'span': 8},
                            {'key': 'license_expiry', 'label': '许可到期日期', 'widget': 'date', 'required': False, 'sort_order': 7, 'span': 8},
                            {'key': 'platform', 'label': '运行平台', 'widget': 'text', 'required': False, 'sort_order': 8, 'span': 8},
                            {'key': 'installed_device', 'label': '安装设备', 'widget': 'textarea', 'required': False, 'sort_order': 9, 'span': 24},
                        ],
                    },
                ]),
            )

        # ============================
        # 7. IT耗材 (root) — consumable-specific fields
        # ============================
        consumable = categories.get('consumable')
        if consumable:
            AssetFormTemplate.objects.create(
                category=consumable,
                name='IT耗材默认模板',
                config=make_config([
                    {
                        'name': '耗材信息',
                        'sort_order': 1,
                        'fields': [
                            {'key': 'consumable_type', 'label': '耗材类型', 'widget': 'select', 'required': False, 'sort_order': 1, 'span': 8,
                             'options': [{'value': 'toner', 'label': '硒鼓'}, {'value': 'cartridge', 'label': '墨盒'}, {'value': 'paper', 'label': '打印纸'}, {'value': 'cable', 'label': '网线'}, {'value': 'fiber', 'label': '光纤跳线'}, {'value': 'keyboard_mouse', 'label': '键盘鼠标'}, {'value': 'disc', 'label': '光盘'}, {'value': 'cable_other', 'label': '线缆'}, {'value': 'other', 'label': '其他'}]},
                            {'key': 'unit', 'label': '单位', 'widget': 'select', 'required': False, 'sort_order': 2, 'span': 8,
                             'options': [{'value': 'piece', 'label': '个'}, {'value': 'box', 'label': '箱'}, {'value': 'pack', 'label': '包'}, {'value': 'roll', 'label': '卷'}, {'value': 'carton', 'label': '盒'}]},
                            {'key': 'current_stock', 'label': '当前库存', 'widget': 'number', 'required': False, 'sort_order': 3, 'span': 8},
                            {'key': 'min_stock', 'label': '最低库存预警', 'widget': 'number', 'required': False, 'sort_order': 4, 'span': 8},
                            {'key': 'unit_price', 'label': '单价', 'widget': 'number', 'required': False, 'sort_order': 5, 'span': 8},
                            {'key': 'last_purchase_date', 'label': '上次采购日期', 'widget': 'date', 'required': False, 'sort_order': 6, 'span': 8},
                            {'key': 'applicable_device', 'label': '适用设备', 'widget': 'textarea', 'required': False, 'sort_order': 7, 'span': 24},
                        ],
                    },
                ]),
            )

        print('Created form templates for 7 categories.')
