<template>
  <div>
    <el-card>
      <template #header><span>部门管理</span><el-button type="primary" size="small" style="float:right" @click="openDialog()">新增部门</el-button></template>
      <el-table :data="tableData" row-key="id" v-loading="loading" default-expand-all :tree-props="{ children: 'children' }">
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="code" label="编码" width="120" />
        <el-table-column prop="manager" label="负责人" width="100" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :title="isEdit ? '编辑部门' : '新增部门'" v-model="visible" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="编码"><el-input v-model="form.code" /></el-form-item>
        <el-form-item label="上级部门"><el-tree-select v-model="form.parent" :data="treeOptions" :props="{ value:'id', label:'name' }" placeholder="无" clearable check-strictly style="width:100%" /></el-form-item>
        <el-form-item label="负责人"><el-input v-model="form.manager" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
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
import { getDepartments, createDepartment, updateDepartment, deleteDepartment } from '../../api/baseData'

const loading = ref(false)
const tableData = ref([])
const visible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const treeOptions = ref([])
const form = reactive({ name: '', code: '', parent: null, manager: '', sort_order: 0 })

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getDepartments()
    tableData.value = res.data.results || res.data
    treeOptions.value = res.data.results || res.data
  } finally { loading.value = false }
}

const openDialog = (row) => {
  if (row) {
    isEdit.value = true; editId.value = row.id
    Object.assign(form, { name: row.name, code: row.code, parent: row.parent, manager: row.manager || '', sort_order: row.sort_order || 0 })
  } else {
    isEdit.value = false
    Object.assign(form, { name: '', code: '', parent: null, manager: '', sort_order: 0 })
  }
  visible.value = true
}

const handleSave = async () => {
  try {
    if (isEdit.value) { await updateDepartment(editId.value, form) } else { await createDepartment(form) }
    ElMessage.success('保存成功'); visible.value = false; fetchData()
  } catch { ElMessage.error('保存失败') }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除吗？', '确认', { type: 'warning' })
    await deleteDepartment(row.id); ElMessage.success('删除成功'); fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>
