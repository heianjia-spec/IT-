<template>
  <div>
    <el-card>
      <template #header><span>{{ title }}</span><el-button type="primary" size="small" style="float:right" @click="openDialog()">新增</el-button></template>
      <el-table :data="tableData.results || []" v-loading="loading" stripe>
        <el-table-column v-for="col in columns" :key="col.prop" :prop="col.prop" :label="col.label" :width="col.width" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="tableData.count" v-model:current-page="page" :page-size="50" :total="tableData.count" layout="total, prev, pager, next" @current-change="fetchData" style="margin-top:16px;justify-content:flex-end" />
    </el-card>
    <el-dialog :title="isEdit ? '编辑' : '新增'" v-model="visible" width="500px">
      <el-form :model="form" label-width="80px">
        <template v-for="f in formFields" :key="f.prop">
          <el-form-item :label="f.label">
            <el-select v-if="f.type==='select'" v-model="form[f.prop]" style="width:100%">
              <el-option v-for="o in f.options" :key="o.value" :label="o.label" :value="o.value" />
            </el-select>
            <el-input v-else-if="f.type==='textarea'" v-model="form[f.prop]" type="textarea" />
            <el-input v-else v-model="form[f.prop]" />
          </el-form-item>
        </template>
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

const props = defineProps({
  title: String,
  columns: Array,
  fetch: Function,
  save: Function,
  del: Function,
  formFields: Array,
})

const loading = ref(false)
const tableData = ref({})
const visible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const page = ref(1)

const form = reactive({})

const fetchData = async () => {
  loading.value = true
  try { const res = await props.fetch({ page: page.value, page_size: 50 }); tableData.value = res.data } finally { loading.value = false }
}

const openDialog = (row) => {
  for (const f of props.formFields) { form[f.prop] = row ? (row[f.prop] || '') : '' }
  if (row) { isEdit.value = true; editId.value = row.id } else { isEdit.value = false }
  visible.value = true
}

const handleSave = async () => {
  try {
    await props.save(isEdit.value, editId.value, { ...form })
    ElMessage.success('保存成功'); visible.value = false; fetchData()
  } catch { ElMessage.error('保存失败') }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '确认', { type: 'warning' })
    await props.del(row.id); ElMessage.success('删除成功'); fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>
