<template>
  <div>
    <el-card>
      <template #header>
        <span>操作日志</span>
        <el-select
          v-model="filterType"
          placeholder="全部类型"
          clearable
          size="small"
          style="width:140px;margin-left:12px"
          @change="fetchData"
        >
          <el-option label="全部类型" value="" />
          <el-option v-for="(v,k) in ACTION_MAP" :key="k" :label="v" :value="k" />
        </el-select>
      </template>
      <el-table :data="tableData.results || []" v-loading="loading" stripe size="small">
        <el-table-column prop="user_name" label="操作人" width="100" />
        <el-table-column label="操作类型" width="110">
          <template #default="{ row }">
            <el-tag :type="getTagType(row.action_type)" size="small">
              {{ row.action_type_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作详情" show-overflow-tooltip />
        <el-table-column prop="asset_count" label="数量" width="60" />
        <el-table-column prop="ip_address" label="IP地址" width="140" />
        <el-table-column prop="created_at" label="操作时间" width="160" />
      </el-table>
      <el-pagination
        v-if="tableData.count"
        v-model:current-page="page"
        :page-size="50"
        :total="tableData.count"
        layout="total, prev, pager, next"
        @current-change="fetchData"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getOperationLogs } from '../../api/assets'

const ACTION_MAP = {
  create: '新增资产', update: '编辑资产', delete: '删除资产',
  batch_delete: '批量删除', import: '导入资产', export: '导出资产',
}

const loading = ref(false)
const tableData = ref({})
const page = ref(1)
const filterType = ref('')

const getTagType = (type) => {
  if (type === 'create' || type === 'import') return 'success'
  if (type === 'delete' || type === 'batch_delete') return 'danger'
  if (type === 'export') return 'info'
  return ''
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = { page: page.value, page_size: 50 }
    if (filterType.value) params.action_type = filterType.value
    const res = await getOperationLogs(params)
    tableData.value = res.data
  } finally { loading.value = false }
}

onMounted(fetchData)
</script>
