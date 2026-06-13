<template>
  <div>
    <el-card>
      <template #header><span>资产分类</span><el-button type="primary" size="small" style="float:right" @click="openDialog()">新增分类</el-button></template>
      <el-table :data="tableData" row-key="id" v-loading="loading" default-expand-all :tree-props="{ children: 'children' }">
        <el-table-column prop="name" label="名称" min-width="150" />
        <el-table-column prop="code" label="编码" width="150" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openDialog(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <CategoryDialog ref="dialogRef" @saved="fetchData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getCategories, deleteCategory } from '../../api/baseData'
import CategoryDialog from './CategoryDialog.vue'

const loading = ref(false)
const tableData = ref([])
const dialogRef = ref(null)

const fetchData = async () => {
  loading.value = true
  try { const res = await getCategories(); tableData.value = res.data.results || res.data } finally { loading.value = false }
}

const openDialog = (row) => { dialogRef.value.open(row) }

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该分类吗？', '确认', { type: 'warning' })
    await deleteCategory(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch { /* cancelled */ }
}

onMounted(fetchData)
</script>
