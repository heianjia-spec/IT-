<template>
  <div>
    <el-card>
      <template #header><span>告警规则</span><el-button type="primary" size="small" style="float:right" @click="openDialog()">新增规则</el-button></template>
      <el-table :data="tableData.results || []" v-loading="loading" stripe>
        <el-table-column prop="name" label="规则名称" width="180" />
        <el-table-column prop="event_type_display" label="事件类型" width="120" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }"><el-switch :model-value="row.is_enabled" disabled size="small" /></template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :title="isEdit ? '编辑规则' : '新增规则'" v-model="visible" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="事件类型">
          <el-select v-model="form.event_type" style="width:100%">
            <el-option v-for="(v,k) in EVENT_MAP" :key="k" :label="v" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用"><el-switch v-model="form.is_enabled" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getAlertRules, createAlertRule, updateAlertRule, deleteAlertRule } from '../../api/alerts'

const EVENT_MAP = { asset_created: '资产新增', status_changed: '资产异动', warranty_expiry: '维保到期', license_expiry: '许可证到期', low_stock: '低库存' }

const loading = ref(false)
const tableData = ref({})
const visible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = reactive({ name: '', event_type: 'warranty_expiry', is_enabled: true, description: '' })

const fetchData = async () => {
  loading.value = true
  try { const res = await getAlertRules({ page_size: 200 }); tableData.value = res.data } finally { loading.value = false }
}

const openDialog = (row) => {
  if (row) { isEdit.value = true; editId.value = row.id; Object.assign(form, row) }
  else { isEdit.value = false; Object.assign(form, { name: '', event_type: 'warranty_expiry', is_enabled: true, description: '' }) }
  visible.value = true
}

const handleSave = async () => {
  try {
    if (isEdit.value) { await updateAlertRule(editId.value, form) } else { await createAlertRule(form) }
    ElMessage.success('保存成功'); visible.value = false; fetchData()
  } catch { ElMessage.error('保存失败') }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '确认', { type: 'warning' })
    await deleteAlertRule(row.id); ElMessage.success('删除成功'); fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>
