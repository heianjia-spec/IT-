<template>
  <div>
    <el-card>
      <template #header>
        <span>告警日志</span>
        <el-button size="small" style="float:right" @click="handleMarkAll">全部已读</el-button>
      </template>
      <el-table :data="tableData.results || []" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" width="180" />
        <el-table-column prop="asset_name" label="关联资产" width="150" />
        <el-table-column prop="message" label="消息内容" show-overflow-tooltip />
        <el-table-column label="状态" width="80">
          <template #default="{ row }"><el-tag :type="row.is_read ? 'info' : 'warning'" size="small">{{ row.is_read ? '已读' : '未读' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button v-if="!row.is_read" link type="primary" size="small" @click="handleMark(row)">标记已读</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination v-if="tableData.count" v-model:current-page="page" :page-size="50" :total="tableData.count" layout="total, prev, pager, next" @current-change="fetchData" style="margin-top:16px;justify-content:flex-end" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getAlertLogs, markRead, markAllRead } from '../../api/alerts'

const loading = ref(false)
const tableData = ref({})
const page = ref(1)

const fetchData = async () => {
  loading.value = true
  try { const res = await getAlertLogs({ page: page.value, page_size: 50 }); tableData.value = res.data } finally { loading.value = false }
}

const handleMark = async (row) => { await markRead(row.id); fetchData() }
const handleMarkAll = async () => { await markAllRead(); ElMessage.success('全部标记为已读'); fetchData() }

onMounted(fetchData)
</script>
