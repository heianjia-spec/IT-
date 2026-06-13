<template>
  <div>
    <el-card>
      <template #header><span>用户管理</span><el-button type="primary" size="small" style="float:right" @click="openDialog()">新增用户</el-button></template>
      <el-table :data="tableData.results || []" v-loading="loading" stripe>
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="first_name" label="姓名" width="100" />
        <el-table-column prop="role_display" label="角色" width="100" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="department_name" label="部门" width="130" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.is_active ? 'success' : 'danger'" size="small">{{ row.is_active ? '启用' : '禁用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="warning" size="small" @click="handleResetPwd(row)">重置密码</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="tableData.count" v-model:current-page="page" :page-size="50" :total="tableData.count" layout="total, prev, pager, next" @current-change="fetchData" style="margin-top:16px;justify-content:flex-end" />
    </el-card>
    <el-dialog :title="isEdit ? '编辑用户' : '新增用户'" v-model="visible" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名"><el-input v-model="form.username" :disabled="isEdit" /></el-form-item>
        <el-form-item v-if="!isEdit" label="密码"><el-input v-model="form.password" type="password" placeholder="默认123456" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="form.first_name" /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width:100%">
            <el-option v-for="(v,k) in ROLE_MAP" :key="k" :label="v" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="部门"><el-tree-select v-model="form.department" :data="deptOptions" :props="{ value:'id', label:'name' }" placeholder="请选择" clearable check-strictly style="width:100%" /></el-form-item>
        <el-form-item label="启用"><el-switch v-model="form.is_active" /></el-form-item>
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
import { getUsers, createUser, updateUser, deleteUser, resetPassword } from '../../api/users'
import { getDepartments } from '../../api/baseData'
import { ROLE_MAP } from '../../utils/constants'

const loading = ref(false)
const tableData = ref({})
const visible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const page = ref(1)
const deptOptions = ref([])
const form = reactive({ username: '', password: '', first_name: '', role: 'user', phone: '', department: null, is_active: true })

const fetchData = async () => {
  loading.value = true
  try { const res = await getUsers({ page: page.value, page_size: 50 }); tableData.value = res.data } finally { loading.value = false }
}

const openDialog = (row) => {
  if (row) { isEdit.value = true; editId.value = row.id; Object.assign(form, { ...row, password: '' }) }
  else { isEdit.value = false; Object.assign(form, { username: '', password: '', first_name: '', role: 'user', phone: '', department: null, is_active: true }) }
  visible.value = true
}

const handleSave = async () => {
  try {
    const data = { ...form }
    if (isEdit.value) { delete data.password; await updateUser(editId.value, data) }
    else { await createUser(data) }
    ElMessage.success('保存成功'); visible.value = false; fetchData()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该用户吗？', '确认', { type: 'warning' })
    await deleteUser(row.id); ElMessage.success('删除成功'); fetchData()
  } catch { /* cancelled */ }
}

const handleResetPwd = async (row) => {
  try {
    await ElMessageBox.confirm(`确定重置 ${row.username} 的密码为 123456 吗？`, '确认', { type: 'warning' })
    await resetPassword(row.id, '123456'); ElMessage.success('密码已重置')
  } catch { /* cancelled */ }
}

onMounted(async () => {
  const deptRes = await getDepartments()
  deptOptions.value = deptRes.data.results || deptRes.data
  fetchData()
})
</script>
