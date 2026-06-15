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

      <!-- Dynamic type-specific fields from template -->
      <DynamicFormRenderer
        v-if="templateConfig.sections.length"
        v-model="form"
        :template-config="templateConfig"
        :context="{ asset_type: derivedType, status: form.status }"
        :data-sources="templateDataSources"
      />

      <!-- Submit -->
      <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      <el-button @click="$router.push('/assets')">取消</el-button>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createAsset, updateAsset, getAsset } from '../../api/assets'
import { getCategories, getDepartments, getLocations, getSuppliers } from '../../api/baseData'
import { ASSET_TYPES, STATUS_MAP } from '../../utils/constants'
import { useFormTemplate } from '../../composables/useFormTemplate'
import DynamicFormRenderer from '../../components/assets/DynamicFormRenderer.vue'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const categoryOptions = ref([])
const departmentOptions = ref([])
const locations = ref([])
const suppliers = ref([])

const { templateConfig, loading: templateLoading, dataSources: templateDataSources, loadTemplate, loadDataSources } = useFormTemplate()

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
  for (const root of categoryOptions.value) {
    if (findCategoryNode(form.category, [root])) {
      return ROOT_TYPE_MAP[root.name] || ''
    }
  }
  return ''
})

// All possible type-specific fields across all asset types
const ALL_TYPE_FIELDS = [
  // Hardware
  'cpu_model','memory_info','disk_size','os','has_monitor','monitor_model','oob_address','nic_info','ip_address','mac_address','port_count','firmware',
  // Printer
  'printer_type','is_color','is_duplex','connect_type','cartridge_model',
  // Network
  'network_type','port_type','poe_support','poe_power','stackable','stack_id','redundancy_power','rack_position',
  // Software
  'software_type','version','license_type','license_key','license_count','used_count','license_expiry','platform','installed_device',
  // Consumable
  'consumable_type','unit','current_stock','min_stock','applicable_device','unit_price','last_purchase_date',
]

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

// Load form template when category changes
watch(() => form.category, (newCategoryId) => {
  loadTemplate(newCategoryId)
})

const handleSave = async () => {
  saving.value = true
  try {
    const data = { ...form }
    data.asset_type = derivedType.value  // Auto-set from category

    // Clean up ALL type-specific fields, they'll be set via the template
    // The dynamic fields in the active template will have valid values,
    // fields not in the template will still be in `data` from getDefaultForm.
    // We keep them since the backend ignores empty strings for non-applicable types.
    // But we DO want to clear null values for cleaner payload:
    for (const key of Object.keys(data)) {
      if (data[key] === null || data[key] === '') {
        delete data[key]
      }
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
  await Promise.all([loadOptions(), loadDataSources()])
  if (isEdit.value) {
    const res = await getAsset(route.params.id)
    Object.assign(form, res.data)
    // Load template for the edited asset's category
    if (form.category) {
      await loadTemplate(form.category)
    }
  }
})
</script>
