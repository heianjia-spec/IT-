<template>
  <div class="dashboard">
    <!-- Clock -->
    <div class="clock-bar">
      <span class="clock-date">{{ dateText }}</span>
      <span class="clock-time">{{ timeText }}</span>
    </div>

    <!-- Summary Cards -->
    <el-row :gutter="16" class="summary-cards">
      <el-col :span="4" v-for="card in cards" :key="card.key">
        <el-card shadow="hover" :style="{ borderLeft: `4px solid ${card.color}` }">
          <div class="card-content">
            <div class="card-value">{{ card.value }}</div>
            <div class="card-label">{{ card.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row -->
    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="8">
        <el-card header="按资产类型统计">
          <v-chart :option="categoryOption" style="height:280px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>按资产状态统计</span>
            <el-select
              v-model="statusFilterType"
              placeholder="全部类型"
              size="small"
              clearable
              style="width:130px;margin-left:12px"
              @change="fetchStatus"
            >
              <el-option label="全部类型" value="" />
              <el-option v-for="(v,k) in ASSET_TYPES" :key="k" :label="v.label" :value="k" />
            </el-select>
          </template>
          <v-chart :option="statusOption" style="height:280px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card header="按部门统计（Top 10）">
          <v-chart :option="deptOption" style="height:280px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Expiry Reminders -->
    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="12">
        <el-card header="维保到期提醒">
          <el-table :data="warrantyExpiring" v-loading="loading" empty-text="暂无即将到期的维保" size="small">
            <el-table-column prop="asset_number" label="资产编号" width="160" />
            <el-table-column prop="name" label="资产名称" show-overflow-tooltip />
            <el-table-column prop="warranty_expiry" label="到期日期" width="120" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="许可证到期提醒">
          <el-table :data="licenseExpiring" v-loading="loading" empty-text="暂无即将到期的许可证" size="small">
            <el-table-column prop="asset_number" label="资产编号" width="160" />
            <el-table-column prop="name" label="软件名称" show-overflow-tooltip />
            <el-table-column prop="license_expiry" label="到期日期" width="120" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { PieChart, BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getSummary, getByCategory, getByStatus, getByDepartment, getExpiryReminders } from '../../api/dashboard'
import { STATUS_MAP, ASSET_TYPES } from '../../utils/constants'

use([PieChart, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer])

const loading = ref(false)
const statusFilterType = ref('')

// 6 summary cards
const cards = reactive([
  { key: 'total',    label: '资产总数', value: 0, color: '#409EFF' },
  { key: 'in_use',   label: '在用',     value: 0, color: '#67C23A' },
  { key: 'in_stock', label: '在库',     value: 0, color: '#909399' },
  { key: 'borrowed', label: '借用',     value: 0, color: '#E6A23C' },
  { key: 'repair',   label: '维修',     value: 0, color: '#F56C6C' },
  { key: 'scrapped', label: '报废',     value: 0, color: '#303133' },
])

// Category pie — show count on label
const categoryOption = reactive({
  tooltip: { trigger: 'item', formatter: '{b}: {c} 台 ({d}%)' },
  legend: { bottom: 0, textStyle: { fontSize: 11 } },
  series: [{
    type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
    label: { show: true, formatter: '{b}\n{c} 台', fontSize: 12 },
    emphasis: { label: { fontSize: 16, fontWeight: 'bold' } },
    data: [],
  }],
})

// Status pie
const statusOption = reactive({
  tooltip: { trigger: 'item', formatter: '{b}: {c} 台 ({d}%)' },
  legend: { bottom: 0, textStyle: { fontSize: 11 } },
  series: [{
    type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
    label: { show: true, formatter: '{b}\n{c} 台', fontSize: 12 },
    data: [],
  }],
})

// Department bar chart
const deptOption = reactive({
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
  grid: { left: '3%', right: '10%', bottom: '3%', top: '8%', containLabel: true },
  xAxis: { type: 'value' },
  yAxis: { type: 'category', data: [], inverse: true, axisLabel: { fontSize: 11 } },
  series: [{
    type: 'bar', data: [], itemStyle: { color: '#409EFF' }, barMaxWidth: 24,
    label: { show: true, position: 'right', fontSize: 12 },
  }],
})

const warrantyExpiring = ref([])
const licenseExpiring = ref([])

// Real-time clock
const timeText = ref('')
const dateText = ref('')
let timer = null

const updateClock = () => {
  const now = new Date()
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  dateText.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 星期${weekdays[now.getDay()]}`
  timeText.value = now.toLocaleTimeString('zh-CN', { hour12: false })
}

onUnmounted(() => { if (timer) clearInterval(timer) })

const updateStatusChart = (data) => {
  statusOption.series[0].data = data.map(d => ({
    name: STATUS_MAP[d.status]?.label || d.status,
    value: d.count,
    itemStyle: { color: STATUS_MAP[d.status]?.color },
  }))
}

const fetchStatus = async () => {
  try {
    const params = {}
    if (statusFilterType.value) params.asset_type = statusFilterType.value
    const res = await getByStatus(params)
    updateStatusChart(res.data)
  } catch { /* ignore */ }
}

const updateCategoryChart = (data) => {
  categoryOption.series[0].data = data.map(d => ({
    name: d.type_display || d.asset_type, value: d.count,
  }))
}

onMounted(async () => {
  updateClock()
  timer = setInterval(updateClock, 1000)
  loading.value = true
  try {
    const [summary, byCategory, byStatus, byDept, expiry] = await Promise.all([
      getSummary(), getByCategory(), getByStatus(), getByDepartment(), getExpiryReminders(),
    ])

    // Summary cards
    cards.forEach(c => { c.value = summary.data[c.key] || 0 })

    // Category pie
    updateCategoryChart(byCategory.data)

    // Status pie
    updateStatusChart(byStatus.data)

    // Department bar
    const deptData = (byDept.data || [])
      .filter(d => d.department__name)
      .sort((a, b) => b.count - a.count)
      .slice(0, 10)
    deptOption.yAxis.data = deptData.map(d => d.department__name)
    deptOption.series[0].data = deptData.map(d => d.count)

    // Expiry reminders
    warrantyExpiring.value = expiry.data.warranty_expiring || []
    licenseExpiring.value = expiry.data.license_expiring || []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.summary-cards .el-card { cursor: default; }
.card-content { text-align: center; padding: 4px 0; }
.card-value { font-size: 28px; font-weight: 700; color: #303133; line-height: 1.2; }
.card-label { font-size: 13px; color: #909399; margin-top: 4px; }
.clock-bar { text-align: right; margin-bottom: 16px; }
.clock-date { font-size: 14px; color: #909399; margin-right: 16px; }
.clock-time { font-size: 24px; font-weight: 700; color: #409EFF; font-family: 'Consolas', 'Monaco', monospace; letter-spacing: 1px; }
</style>
