// Asset type definitions with their specialized fields
export const ASSET_TYPES = {
  server: {
    label: '服务器',
    category: 'hw_server',
    fields: ['cpu_model', 'memory_info', 'disk_size', 'os', 'oob_address', 'nic_info', 'ip_address', 'mac_address', 'redundancy_power', 'rack_position'],
  },
  pc: {
    label: 'PC',
    category: 'hw_pc',
    fields: ['cpu_model', 'memory_info', 'disk_size', 'os', 'has_monitor', 'monitor_model', 'ip_address', 'mac_address'],
  },
  printer: {
    label: '打印机',
    category: 'hw_printer',
    fields: ['printer_type', 'is_color', 'is_duplex', 'connect_type', 'cartridge_model', 'ip_address', 'mac_address', 'port_count', 'firmware'],
  },
  network_device: {
    label: '网络设备',
    category: 'hw_network',
    fields: ['network_type', 'ip_address', 'mac_address', 'port_count', 'firmware', 'port_type', 'poe_support', 'poe_power', 'redundancy_power', 'rack_position'],
  },
  switch: {
    label: '交换机',
    category: 'hw_switch',
    fields: ['network_type', 'ip_address', 'mac_address', 'port_count', 'firmware', 'port_type', 'poe_support', 'poe_power', 'stackable', 'stack_id', 'redundancy_power', 'rack_position'],
  },
  software: {
    label: '软件',
    category: 'software',
    fields: ['software_type', 'version', 'license_type', 'license_key', 'license_count', 'used_count', 'license_expiry', 'platform', 'installed_device'],
  },
  consumable: {
    label: '耗材',
    category: 'consumable',
    fields: ['consumable_type', 'unit', 'current_stock', 'min_stock', 'applicable_device', 'unit_price', 'last_purchase_date'],
  },
}

export const STATUS_MAP = {
  in_stock: { label: '在库', color: '#409EFF' },
  in_use: { label: '在用', color: '#67C23A' },
  borrowed: { label: '借用', color: '#8B5CF6' },
  repair: { label: '维修', color: '#E6A23C' },
  scrapped: { label: '报废', color: '#F56C6C' },
  transferring: { label: '调拨中', color: '#909399' },
}

export const ROLE_MAP = {
  admin: '管理员',
  asset_manager: '资产管理员',
  user: '普通用户',
  viewer: '只读用户',
}

export const PRINTER_TYPE_MAP = {
  laser: '激光', inkjet: '喷墨', dot_matrix: '针式', mfp: '多功能一体机',
}

export const CONNECT_TYPE_MAP = {
  usb: 'USB', wired: '有线网络', wifi: 'WiFi',
}

export const NETWORK_TYPE_MAP = {
  router: '路由器', firewall: '防火墙', switch_dev: '交换机',
  load_balancer: '负载均衡', wireless_controller: '无线控制器', vpn_gateway: 'VPN网关',
}

export const SOFTWARE_TYPE_MAP = {
  os: '操作系统', office: '办公软件', database: '数据库', middleware: '中间件',
  security: '安全软件', design: '设计软件', business: '业务应用', dev_tool: '开发工具', other: '其他',
}

export const LICENSE_TYPE_MAP = {
  perpetual: '永久授权', subscription: '订阅制', opensource: '开源', self_developed: '自研',
}

export const CONSUMABLE_TYPE_MAP = {
  toner: '硒鼓', cartridge: '墨盒', paper: '打印纸', cable: '网线',
  fiber: '光纤跳线', keyboard_mouse: '键盘鼠标', disc: '光盘', cable_other: '线缆', other: '其他',
}

export const UNIT_MAP = {
  piece: '个', box: '箱', pack: '包', roll: '卷', carton: '盒',
}

// Label size options
export const LABEL_SIZES = [
  { value: '60x40', label: '60×40mm' },
  { value: '80x50', label: '80×50mm' },
  { value: '100x70', label: '100×70mm' },
]
