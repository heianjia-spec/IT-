"""
Field registry — defines all available asset fields for form template configuration.

Each entry maps an Asset model field key to its metadata:
  - key:       Model field name (must match Asset model)
  - label:     Default display label in Chinese
  - widget:    Default widget type
  - category:  Grouping category for the template editor ("hardware" / "software" / "consumable")
  - options:   Predefined select options (null if not a select widget)
"""

FIELD_REGISTRY = {
    # ==================== Hardware Common ====================
    'cpu_model': {
        'key': 'cpu_model', 'label': 'CPU型号', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'memory_info': {
        'key': 'memory_info', 'label': '内存', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'disk_size': {
        'key': 'disk_size', 'label': '硬盘', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'os': {
        'key': 'os', 'label': '操作系统', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'oob_address': {
        'key': 'oob_address', 'label': '管理地址(OOB)', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'nic_info': {
        'key': 'nic_info', 'label': '网卡信息', 'widget': 'textarea',
        'category': 'hardware', 'options': None,
    },
    'ip_address': {
        'key': 'ip_address', 'label': 'IP地址/管理地址', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'mac_address': {
        'key': 'mac_address', 'label': 'MAC地址', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'port_count': {
        'key': 'port_count', 'label': '端口数量', 'widget': 'number',
        'category': 'hardware', 'options': None,
    },
    'firmware': {
        'key': 'firmware', 'label': '固件版本', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'has_monitor': {
        'key': 'has_monitor', 'label': '是否带显示器', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'monitor_model': {
        'key': 'monitor_model', 'label': '显示器型号', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'redundancy_power': {
        'key': 'redundancy_power', 'label': '是否冗余电源', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'rack_position': {
        'key': 'rack_position', 'label': '机架位置', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },

    # ==================== Printer-specific ====================
    'printer_type': {
        'key': 'printer_type', 'label': '打印机类型', 'widget': 'select',
        'category': 'hardware',
        'options': [
            {'value': 'laser', 'label': '激光'},
            {'value': 'inkjet', 'label': '喷墨'},
            {'value': 'dot_matrix', 'label': '针式'},
            {'value': 'mfp', 'label': '多功能一体机'},
        ],
    },
    'is_color': {
        'key': 'is_color', 'label': '是否彩色', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'is_duplex': {
        'key': 'is_duplex', 'label': '是否双面打印', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'connect_type': {
        'key': 'connect_type', 'label': '连接方式', 'widget': 'select',
        'category': 'hardware',
        'options': [
            {'value': 'usb', 'label': 'USB'},
            {'value': 'wired', 'label': '有线网络'},
            {'value': 'wifi', 'label': 'WiFi'},
        ],
    },
    'cartridge_model': {
        'key': 'cartridge_model', 'label': '硒鼓/墨盒型号', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },

    # ==================== Network-device-specific ====================
    'network_type': {
        'key': 'network_type', 'label': '网络设备类型', 'widget': 'select',
        'category': 'hardware',
        'options': [
            {'value': 'router', 'label': '路由器'},
            {'value': 'firewall', 'label': '防火墙'},
            {'value': 'switch_dev', 'label': '交换机'},
            {'value': 'load_balancer', 'label': '负载均衡'},
            {'value': 'wireless_controller', 'label': '无线控制器'},
            {'value': 'vpn_gateway', 'label': 'VPN网关'},
        ],
    },
    'port_type': {
        'key': 'port_type', 'label': '端口类型', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },
    'poe_support': {
        'key': 'poe_support', 'label': '是否支持PoE', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'poe_power': {
        'key': 'poe_power', 'label': 'PoE功率(W)', 'widget': 'number',
        'category': 'hardware', 'options': None,
    },
    'stackable': {
        'key': 'stackable', 'label': '是否可堆叠', 'widget': 'switch',
        'category': 'hardware', 'options': None,
    },
    'stack_id': {
        'key': 'stack_id', 'label': '堆叠编号', 'widget': 'text',
        'category': 'hardware', 'options': None,
    },

    # ==================== Software-specific ====================
    'software_type': {
        'key': 'software_type', 'label': '软件类型', 'widget': 'select',
        'category': 'software',
        'options': [
            {'value': 'os', 'label': '操作系统'},
            {'value': 'office', 'label': '办公软件'},
            {'value': 'database', 'label': '数据库'},
            {'value': 'middleware', 'label': '中间件'},
            {'value': 'security', 'label': '安全软件'},
            {'value': 'design', 'label': '设计软件'},
            {'value': 'business', 'label': '业务应用'},
            {'value': 'dev_tool', 'label': '开发工具'},
            {'value': 'other', 'label': '其他'},
        ],
    },
    'version': {
        'key': 'version', 'label': '版本号', 'widget': 'text',
        'category': 'software', 'options': None,
    },
    'license_type': {
        'key': 'license_type', 'label': '授权类型', 'widget': 'select',
        'category': 'software',
        'options': [
            {'value': 'perpetual', 'label': '永久授权'},
            {'value': 'subscription', 'label': '订阅制'},
            {'value': 'opensource', 'label': '开源'},
            {'value': 'self_developed', 'label': '自研'},
        ],
    },
    'license_key': {
        'key': 'license_key', 'label': '许可证号', 'widget': 'text',
        'category': 'software', 'options': None,
    },
    'license_count': {
        'key': 'license_count', 'label': '授权数量', 'widget': 'number',
        'category': 'software', 'options': None,
    },
    'used_count': {
        'key': 'used_count', 'label': '已用数量', 'widget': 'number',
        'category': 'software', 'options': None,
    },
    'license_expiry': {
        'key': 'license_expiry', 'label': '许可到期日期', 'widget': 'date',
        'category': 'software', 'options': None,
    },
    'platform': {
        'key': 'platform', 'label': '运行平台', 'widget': 'text',
        'category': 'software', 'options': None,
    },
    'installed_device': {
        'key': 'installed_device', 'label': '安装设备', 'widget': 'textarea',
        'category': 'software', 'options': None,
    },

    # ==================== Consumable-specific ====================
    'consumable_type': {
        'key': 'consumable_type', 'label': '耗材类型', 'widget': 'select',
        'category': 'consumable',
        'options': [
            {'value': 'toner', 'label': '硒鼓'},
            {'value': 'cartridge', 'label': '墨盒'},
            {'value': 'paper', 'label': '打印纸'},
            {'value': 'cable', 'label': '网线'},
            {'value': 'fiber', 'label': '光纤跳线'},
            {'value': 'keyboard_mouse', 'label': '键盘鼠标'},
            {'value': 'disc', 'label': '光盘'},
            {'value': 'cable_other', 'label': '线缆'},
            {'value': 'other', 'label': '其他'},
        ],
    },
    'unit': {
        'key': 'unit', 'label': '单位', 'widget': 'select',
        'category': 'consumable',
        'options': [
            {'value': 'piece', 'label': '个'},
            {'value': 'box', 'label': '箱'},
            {'value': 'pack', 'label': '包'},
            {'value': 'roll', 'label': '卷'},
            {'value': 'carton', 'label': '盒'},
        ],
    },
    'current_stock': {
        'key': 'current_stock', 'label': '当前库存', 'widget': 'number',
        'category': 'consumable', 'options': None,
    },
    'min_stock': {
        'key': 'min_stock', 'label': '最低库存预警', 'widget': 'number',
        'category': 'consumable', 'options': None,
    },
    'applicable_device': {
        'key': 'applicable_device', 'label': '适用设备', 'widget': 'textarea',
        'category': 'consumable', 'options': None,
    },
    'unit_price': {
        'key': 'unit_price', 'label': '单价', 'widget': 'number',
        'category': 'consumable', 'options': None,
    },
    'last_purchase_date': {
        'key': 'last_purchase_date', 'label': '上次采购日期', 'widget': 'date',
        'category': 'consumable', 'options': None,
    },
}
