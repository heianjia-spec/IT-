<template>
  <div class="asset-form">
    <el-page-header :content="isEdit ? '编辑资产' : '新增资产'" @back="$router.push('/assets')" />

    <el-form ref="formRef" :model="form" label-width="110px" style="margin-top:20px;max-width:900px">
      <!-- Basic Info -->
      <el-card header="基本信息" style="margin-bottom:16px">
        <el-form-item label="资产分类" required>
          <el-cascader v-model="form.category" :options="categoryOptions" :props="{ value:'id', label:'name', checkStrictly:true, emitPath:false }" placeholder="请选择资产分类" clearable style="width:280px" />
          <span v-if="derivedType" style="margin-left:12px;color:#909399;font-size:13px">
            表单类型：<el-tag size="small">{{ ASSET_TYPES[derivedType]?.label }}</el-tag>
          </span>
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="资产编号">
              <el-input v-model="form.asset_number" placeholder="自动生成" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="资产名称">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="NC编号">
              <el-input v-model="form.nc_number" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="品牌">
              <el-input v-model="form.brand" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="规格型号">
              <el-input v-model="form.spec_model" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="序列号/SN">
              <el-input v-model="form.serial_number" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="资产状态">
              <el-select v-model="form.status" style="width:100%">
                <el-option v-for="(v,k) in STATUS_MAP" :key="k" :label="v.label" :value="k" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="备注">
              <el-input v-model="form.remarks" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Ownership -->
      <el-card header="归属信息" style="margin-bottom:16px">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="使用部门">
              <el-tree-select v-model="form.department" :data="departmentOptions" :props="{ value:'id', label:'name' }" placeholder="请选择" clearable check-strictly style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="责任人">
              <el-input v-model="form.responsible_person" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="存放位置">
              <el-select v-model="form.location" placeholder="请选择" clearable style="width:100%">
                <el-option v-for="loc in locations" :key="loc.id" :label="loc.name" :value="loc.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16" v-if="form.status === 'in_use'">
          <el-col :span="8">
            <el-form-item label="机房名称">
              <el-input v-model="form.room_name" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="机柜编号">
              <el-input v-model="form.cabinet_no" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16" v-if="form.status === 'in_stock'">
          <el-col :span="8">
            <el-form-item label="存放位置描述">
              <el-input v-model="form.storage_location" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Purchase -->
      <el-card header="采购信息" style="margin-bottom:16px">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="购置日期">
              <el-date-picker v-model="form.purchase_date" type="date" placeholder="选择日期" style="width:100%" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="生产日期">
              <el-date-picker v-model="form.production_date" type="date" placeholder="选择日期" style="width:100%" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="购置金额(元)">
              <el-input-number v-model="form.purchase_amount" :min="0" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="折旧年限">
              <el-input-number v-model="form.depreciation_years" :min="0" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="供应商">
              <el-select v-model="form.supplier" placeholder="请选择" clearable style="width:100%">
                <el-option v-for="s in suppliers" :key="s.id" :label="s.name" :value="s.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="保修截止日期">
              <el-date-picker v-model="form.warranty_expiry" type="date" placeholder="选择日期" style="width:100%" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Hardware Fields (Dynamic) -->
      <el-card v-if="derivedType && ['server','pc','printer','network_device','switch'].includes(derivedType)" header="硬件信息" style="margin-bottom:16px">
        <el-row :gutter="16">
          <template v-for="f in currentTypeFields" :key="f">
            <el-col :span="f === 'nic_info' || f === 'installed_device' || f === 'applicable_device' ? 24 : 8">
              <!-- cpu_model, memory_info, disk_size, os, oob_address, ip_address, mac_address, firmware, rack_position, stack_id, cartridge_model, monitor_model -->
              <el-form-item v-if="['cpu_model','memory_info','disk_size','os','oob_address','ip_address','mac_address','firmware','rack_position','stack_id','cartridge_model','monitor_model'].includes(f)" :label="getFieldLabel(f)">
                <el-input v-model="form[f]" />
              </el-form-item>
              <!-- port_count, poe_power -->
              <el-form-item v-else-if="['port_count','poe_power'].includes(f)" :label="getFieldLabel(f)">
                <el-input-number v-model="form[f]" :min="0" style="width:100%" />
              </el-form-item>
              <!-- has_monitor, is_color, is_duplex, poe_support, stackable, redundancy_power -->
              <el-form-item v-else-if="['has_monitor','is_color','is_duplex','poe_support','stackable','redundancy_power'].includes(f)" :label="getFieldLabel(f)">
                <el-switch v-model="form[f]" />
              </el-form-item>
              <!-- printer_type, connect_type -->
              <el-form-item v-else-if="f==='printer_type'" label="打印机类型">
                <el-select v-model="form.printer_type" style="width:100%">
                  <el-option v-for="(v,k) in PRINTER_TYPE_MAP" :key="k" :label="v" :value="k" />
                </el-select>
              </el-form-item>
              <el-form-item v-else-if="f==='connect_type'" label="连接方式">
                <el-select v-model="form.connect_type" style="width:100%">
                  <el-option v-for="(v,k) in CONNECT_TYPE_MAP" :key="k" :label="v" :value="k" />
                </el-select>
              </el-form-item>
              <!-- network_type -->
              <el-form-item v-else-if="f==='network_type'" label="网络设备类型">
                <el-select v-model="form.network_type" style="width:100%">
                  <el-option v-for="(v,k) in NETWORK_TYPE_MAP" :key="k" :label="v" :value="k" />
                </el-select>
              </el-form-item>
              <!-- port_type, nic_info -->
              <el-form-item v-else-if="['port_type','nic_info'].includes(f)" :label="getFieldLabel(f)">
                <el-input v-model="form[f]" type="textarea" :rows="2" />
              </el-form-item>
            </el-col>
          </template>
        </el-row>
      </el-card>

      <!-- Software Fields -->
      <el-card v-if="derivedType === 'software'" header="软件信息" style="margin-bottom:16px">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="软件类型">
              <el-select v-model="form.software_type" style="width:100%">
                <el-option v-for="(v,k) in SOFTWARE_TYPE_MAP" :key="k" :label="v" :value="k" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="版本号"><el-input v-model="form.version" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="授权类型">
              <el-select v-model="form.license_type" style="width:100%">
                <el-option v-for="(v,k) in LICENSE_TYPE_MAP" :key="k" :label="v" :value="k" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="许可证号"><el-input v-model="form.license_key" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="授权数量"><el-input-number v-model="form.license_count" :min="0" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="已用数量"><el-input-number v-model="form.used_count" :min="0" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="许可到期日期">
              <el-date-picker v-model="form.license_expiry" type="date" style="width:100%" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="运行平台"><el-input v-model="form.platform" /></el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="安装设备"><el-input v-model="form.installed_device" type="textarea" :rows="2" /></el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Consumable Fields -->
      <el-card v-if="derivedType === 'consumable'" header="耗材信息" style="margin-bottom:16px">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="耗材类型">
              <el-select v-model="form.consumable_type" style="width:100%">
                <el-option v-for="(v,k) in CONSUMABLE_TYPE_MAP" :key="k" :label="v" :value="k" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单位">
              <el-select v-model="form.unit" style="width:100%">
                <el-option v-for="(v,k) in UNIT_MAP" :key="k" :label="v" :value="k" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="当前库存"><el-input-number v-model="form.current_stock" :min="0" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="最低库存预警"><el-input-number v-model="form.min_stock" :min="0" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="单价"><el-input-number v-model="form.unit_price" :min="0" :precision="2" style="width:100%" /></el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="上次采购日期">
              <el-date-picker v-model="form.last_purchase_date" type="date" style="width:100%" value-format="YYYY-MM-DD" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="适用设备"><el-input v-model="form.applicable_device" type="textarea" :rows="2" /></el-form-item>
          </el-col>
        </el-row>
      </el-card>

      <!-- Submit -->
      <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      <el-button @click="$router.push('/assets')">取消</el-button>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createAsset, updateAsset, getAsset } from '../../api/assets'
import { getCategories, getDepartments, getLocations, getSuppliers } from '../../api/baseData'
import { ASSET_TYPES, STATUS_MAP, PRINTER_TYPE_MAP, CONNECT_TYPE_MAP, NETWORK_TYPE_MAP, SOFTWARE_TYPE_MAP, LICENSE_TYPE_MAP, CONSUMABLE_TYPE_MAP, UNIT_MAP } from '../../utils/constants'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const categoryOptions = ref([])
const departmentOptions = ref([])
const locations = ref([])
const suppliers = ref([])

const getDefaultForm = () => ({
  asset_type: '', asset_number: '', name: '', nc_number: '', category: null, brand: '', spec_model: '', serial_number: '',
  status: 'in_stock', remarks: '', department: null, responsible_person: '', location: null,
  room_name: '', cabinet_no: '', storage_location: '',
  purchase_date: null, production_date: null, purchase_amount: null, depreciation_years: null,
  supplier: null, warranty_expiry: null,
  cpu_model: '', memory_info: '', disk_size: '', os: '', has_monitor: null, monitor_model: '',
  oob_address: '', nic_info: '', ip_address: '', mac_address: '', port_count: null, firmware: '',
  printer_type: '', is_color: null, is_duplex: null, connect_type: '', cartridge_model: '',
  network_type: '', port_type: '', poe_support: null, poe_power: null,
  stackable: null, stack_id: '', redundancy_power: null, rack_position: '',
  software_type: '', version: '', license_type: '', license_key: '', license_count: null,
  used_count: null, license_expiry: null, platform: '', installed_device: '',
  consumable_type: '', unit: '', current_stock: null, min_stock: null,
  applicable_device: '', unit_price: null, last_purchase_date: null,
})
const form = reactive(getDefaultForm())

// Derive asset_type group from category tree
const findCategoryNode = (id, nodes) => {
  for (const n of nodes) {
    if (n.id === id) return n
    if (n.children) { const found = findCategoryNode(id, n.children); if (found) return found }
  }
  return null
}

const ROOT_TYPE_MAP = { '硬件': 'server', '软件': 'software', 'IT耗材': 'consumable' }

const derivedType = computed(() => {
  if (!form.category) return ''
  const node = findCategoryNode(form.category, categoryOptions.value)
  if (!node) return ''
  // Walk up to root by checking which root node contains this one
  for (const root of categoryOptions.value) {
    if (findCategoryNode(form.category, [root])) {
      return ROOT_TYPE_MAP[root.name] || ''
    }
  }
  return ''
})

const isHardware = computed(() => ['server', 'pc', 'printer', 'network_device', 'switch'].includes(derivedType.value))
const currentTypeFields = computed(() => ASSET_TYPES[derivedType.value]?.fields || [])

const FIELD_LABELS = {
  cpu_model: 'CPU型号', memory_info: '内存', disk_size: '硬盘', os: '操作系统',
  oob_address: '管理地址(OOB)', nic_info: '网卡信息', ip_address: 'IP地址', mac_address: 'MAC地址',
  port_count: '端口数量', firmware: '固件版本', has_monitor: '是否带显示器', monitor_model: '显示器型号',
  rack_position: '机架位置', stack_id: '堆叠编号',
  is_color: '是否彩色', is_duplex: '是否双面打印', cartridge_model: '硒鼓/墨盒型号',
  network_type: '网络设备类型', port_type: '端口类型', poe_support: '是否支持PoE', poe_power: 'PoE功率(W)',
  stackable: '是否可堆叠', redundancy_power: '是否冗余电源',
}

const getFieldLabel = (f) => FIELD_LABELS[f] || f

const loadOptions = async () => {
  const [cat, dept, loc, sup] = await Promise.all([
    getCategories(), getDepartments(), getLocations(), getSuppliers(),
  ])
  categoryOptions.value = cat.data.results || cat.data
  departmentOptions.value = dept.data.results || dept.data
  locations.value = loc.data.results || loc.data
  suppliers.value = sup.data.results || sup.data
  // Flatten categories for cascader
  const flatten = (items) => {
    const result = []
    for (const item of items) {
      const node = { ...item, children: item.children?.length ? flatten(item.children) : undefined }
      result.push(node)
    }
    return result
  }
  categoryOptions.value = flatten(cat.data.results || cat.data)
}

const handleSave = async () => {
  saving.value = true
  try {
    const data = { ...form }
    data.asset_type = derivedType.value  // Auto-set from category
    // Clean up type-specific fields not in current type
    if (!isHardware.value) {
      for (const f of ['cpu_model','memory_info','disk_size','os','has_monitor','monitor_model','oob_address','nic_info','ip_address','mac_address','port_count','firmware','printer_type','is_color','is_duplex','connect_type','cartridge_model','network_type','port_type','poe_support','poe_power','stackable','stack_id','redundancy_power','rack_position']) {
        delete data[f]
      }
    }
    if (derivedType.value !== 'software') {
      for (const f of ['software_type','version','license_type','license_key','license_count','used_count','license_expiry','platform','installed_device']) { delete data[f] }
    }
    if (derivedType.value !== 'consumable') {
      for (const f of ['consumable_type','unit','current_stock','min_stock','applicable_device','unit_price','last_purchase_date']) { delete data[f] }
    }
    if (isEdit.value) {
      await updateAsset(route.params.id, data)
    } else {
      await createAsset(data)
    }
    ElMessage.success(isEdit.value ? '保存成功' : '创建成功')
    router.push('/assets')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await loadOptions()
  if (isEdit.value) {
    const res = await getAsset(route.params.id)
    Object.assign(form, res.data)
  }
})
</script>
