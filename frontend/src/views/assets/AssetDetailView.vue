<template>
  <div class="asset-detail" v-loading="loading">
    <el-page-header content="资产详情" @back="$router.push('/assets')">
      <template #extra>
        <el-button type="primary" @click="$router.push(`/assets/${asset.id}/edit`)">编辑</el-button>
        <el-button type="danger" @click="handleDelete">删除</el-button>
        <el-button @click="openLabelDialog">打印标签</el-button>
      </template>
    </el-page-header>

    <!-- Basic Info -->
    <el-card header="基本信息" style="margin-top:20px">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="资产编号">{{ asset.asset_number }}</el-descriptions-item>
        <el-descriptions-item label="资产名称">{{ asset.name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="资产类型">{{ ASSET_TYPES[asset.asset_type]?.label || '-' }}</el-descriptions-item>
        <el-descriptions-item label="品牌">{{ asset.brand || '-' }}</el-descriptions-item>
        <el-descriptions-item label="规格型号">{{ asset.spec_model || '-' }}</el-descriptions-item>
        <el-descriptions-item label="序列号">{{ asset.serial_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="NC编号">{{ asset.nc_number || '-' }}</el-descriptions-item>
        <el-descriptions-item label="资产状态">
          <el-tag :color="STATUS_MAP[asset.status]?.color" effect="dark" style="color:#fff">{{ STATUS_MAP[asset.status]?.label || '-' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注">{{ asset.remarks || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- Ownership -->
    <el-card header="归属信息" style="margin-top:16px">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="使用部门">{{ asset.department_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="责任人">{{ asset.responsible_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="存放位置">{{ asset.location_name || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.status === 'in_use'" label="机房名称">{{ asset.room_name || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.status === 'in_use'" label="机柜编号">{{ asset.cabinet_no || '-' }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.status === 'in_stock'" label="存放位置描述">{{ asset.storage_location || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- Purchase -->
    <el-card header="采购信息" style="margin-top:16px">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="购置日期">{{ asset.purchase_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="生产日期">{{ asset.production_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="购置金额">{{ asset.purchase_amount ? '¥' + asset.purchase_amount : '-' }}</el-descriptions-item>
        <el-descriptions-item label="折旧年限">{{ asset.depreciation_years ? asset.depreciation_years + '年' : '-' }}</el-descriptions-item>
        <el-descriptions-item label="供应商">{{ asset.supplier_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="保修截止日期">{{ asset.warranty_expiry || '-' }}</el-descriptions-item>
        <el-descriptions-item label="保修状态">
          <el-tag v-if="asset.warranty_status==='under_warranty'" type="success">在保</el-tag>
          <el-tag v-else-if="asset.warranty_status==='expired'" type="danger">过保</el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- Hardware/Software/Consumable specific -->
    <el-card v-if="isHardware" header="硬件信息" style="margin-top:16px">
      <el-descriptions :column="3" border>
        <el-descriptions-item v-if="asset.cpu_model" label="CPU型号">{{ asset.cpu_model }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.memory_info" label="内存">{{ asset.memory_info }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.disk_size" label="硬盘">{{ asset.disk_size }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.os" label="操作系统">{{ asset.os }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.has_monitor !== null" label="是否带显示器">{{ asset.has_monitor ? '是' : '否' }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.monitor_model" label="显示器型号">{{ asset.monitor_model }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.oob_address" label="管理地址(OOB)">{{ asset.oob_address }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.nic_info" label="网卡信息" :span="3">{{ asset.nic_info }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.ip_address" label="IP地址">{{ asset.ip_address }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.mac_address" label="MAC地址">{{ asset.mac_address }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.port_count !== null" label="端口数量">{{ asset.port_count }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.firmware" label="固件版本">{{ asset.firmware }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.printer_type" :label="'打印机类型'">{{ PRINTER_TYPE_MAP[asset.printer_type] || asset.printer_type }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.network_type" :label="'网络设备类型'">{{ NETWORK_TYPE_MAP[asset.network_type] || asset.network_type }}</el-descriptions-item>
        <el-descriptions-item v-if="asset.rack_position" label="机架位置">{{ asset.rack_position }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- Status History -->
    <el-card header="状态变更记录" style="margin-top:16px">
      <el-table :data="statusHistory" empty-text="暂无变更记录">
        <el-table-column label="变更前" width="120">
          <template #default="{ row }">{{ row.from_status_display || '-' }}</template>
        </el-table-column>
        <el-table-column label="变更后" width="120">
          <template #default="{ row }">{{ row.to_status_display }}</template>
        </el-table-column>
        <el-table-column prop="changed_by_name" label="操作人" width="120" />
        <el-table-column prop="remarks" label="备注" min-width="200" />
        <el-table-column prop="created_at" label="操作时间" width="160" />
      </el-table>
    </el-card>

    <LabelDialog ref="labelDialogRef" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAsset, deleteAsset, getStatusHistory } from '../../api/assets'
import { ASSET_TYPES, STATUS_MAP, PRINTER_TYPE_MAP, NETWORK_TYPE_MAP } from '../../utils/constants'
import LabelDialog from '../../components/assets/LabelDialog.vue'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const asset = ref({})
const statusHistory = ref([])
const labelDialogRef = ref(null)

const isHardware = computed(() => ['server','pc','printer','network_device','switch'].includes(asset.value.asset_type))

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定删除该资产吗？', '确认删除', { type: 'warning' })
    await deleteAsset(asset.value.id)
    ElMessage.success('删除成功')
    router.push('/assets')
  } catch { /* cancelled */ }
}

const openLabelDialog = () => {
  labelDialogRef.value.open(asset.value)
}

onMounted(async () => {
  loading.value = true
  try {
    const [detail, history] = await Promise.all([
      getAsset(route.params.id),
      getStatusHistory(route.params.id),
    ])
    asset.value = detail.data
    statusHistory.value = history.data
  } finally {
    loading.value = false
  }
})
</script>
