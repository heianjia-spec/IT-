<template>
  <div class="asset-list">
    <!-- Search -->
    <el-card class="search-card">
      <el-form :model="search" inline>
        <el-form-item label="关键字">
          <el-input v-model="search.search" placeholder="编号/名称/序列号" clearable style="width:200px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search.status" placeholder="全部" clearable style="width:120px">
            <el-option v-for="(v,k) in STATUS_MAP" :key="k" :label="v.label" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="资产分类">
          <el-cascader
            v-model="search.category"
            :options="categoryOptions"
            :props="{ value:'id', label:'name', checkStrictly:true, emitPath:false }"
            placeholder="全部"
            clearable
            style="width:200px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="doSearch">查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Actions -->
    <el-card class="action-card">
      <el-button type="primary" @click="$router.push('/assets/add')">新增资产</el-button>
      <el-button @click="showImport = true">导入</el-button>
      <el-button @click="showExport = true">导出</el-button>
      <el-button @click="handleDownloadTemplate">下载模板</el-button>
      <el-button v-if="selectedRows.length" type="warning" @click="handleBatchPrint">批量打印标签 ({{ selectedRows.length }})</el-button>
      <el-button v-if="selectedRows.length" type="danger" @click="handleBatchDelete">批量删除 ({{ selectedRows.length }})</el-button>
    </el-card>

    <!-- Table -->
    <el-card>
      <el-table :data="tableData" v-loading="loading" @selection-change="handleSelectionChange" stripe>
        <el-table-column type="selection" width="40" />
        <el-table-column prop="asset_number" label="资产编号" width="150" />
        <el-table-column prop="name" label="资产名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="asset_type_display" label="类型" width="100" />
        <el-table-column prop="category_name" label="分类" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :color="STATUS_MAP[row.status]?.color" effect="dark" size="small" style="color:#fff">
              {{ STATUS_MAP[row.status]?.label || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="department_name" label="部门" width="120" />
        <el-table-column prop="responsible_person" label="责任人" width="80" />
        <el-table-column prop="warranty_status" label="保修" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.warranty_status==='under_warranty'" type="success" size="small">在保</el-tag>
            <el-tag v-else-if="row.warranty_status==='expired'" type="danger" size="small">过保</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="$router.push(`/assets/${row.id}`)">详情</el-button>
            <el-button link type="primary" size="small" @click="$router.push(`/assets/${row.id}/edit`)">编辑</el-button>
            <el-dropdown trigger="click" @command="(cmd) => handleRowCommand(cmd, row)">
              <el-button link type="primary" size="small" @click.stop>
                更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="label">生成标签</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="fetchData"
          @current-change="fetchData"
        />
      </div>
    </el-card>

    <!-- Import Dialog -->
    <el-dialog v-model="showImport" title="导入资产" width="500px" @close="importResult=null">
      <el-form label-width="100px">
        <el-form-item label="资产类型">
          <el-select v-model="importType" placeholder="请选择">
            <el-option v-for="(v,k) in ASSET_TYPES" :key="k" :label="v.label" :value="k" />
          </el-select>
        </el-form-item>
        <el-form-item label="上传文件">
          <el-upload :auto-upload="false" :limit="1" accept=".xlsx" :on-change="handleFileChange" :file-list="fileList">
            <el-button type="primary">选择文件</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <div v-if="importResult" style="margin-top:12px">
        <el-alert :title="`成功 ${importResult.success_count} 条，失败 ${importResult.error_count} 条`" :type="importResult.error_count ? 'warning' : 'success'" />
      </div>
      <template #footer>
        <el-button @click="showImport = false">取消</el-button>
        <el-button type="primary" :disabled="!uploadFile" @click="handleImport">确认导入</el-button>
      </template>
    </el-dialog>

    <!-- Export Dialog -->
    <el-dialog v-model="showExport" title="导出资产" width="600px">
      <el-checkbox-group v-model="exportFields">
        <el-checkbox label="asset_number">资产编号</el-checkbox>
        <el-checkbox label="name">资产名称</el-checkbox>
        <el-checkbox label="asset_type">资产类型</el-checkbox>
        <el-checkbox label="brand">品牌</el-checkbox>
        <el-checkbox label="spec_model">规格型号</el-checkbox>
        <el-checkbox label="serial_number">序列号</el-checkbox>
        <el-checkbox label="category">资产分类</el-checkbox>
        <el-checkbox label="status">状态</el-checkbox>
        <el-checkbox label="department">部门</el-checkbox>
        <el-checkbox label="responsible_person">责任人</el-checkbox>
        <el-checkbox label="purchase_date">购置日期</el-checkbox>
        <el-checkbox label="remarks">备注</el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <el-button @click="showExport = false">取消</el-button>
        <el-button type="primary" @click="handleExport">导出</el-button>
      </template>
    </el-dialog>

    <!-- Label Dialog -->
    <LabelDialog ref="labelDialogRef" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAssets, deleteAsset, batchDeleteAssets, downloadTemplate, importAssets, exportAssets } from '../../api/assets'
import { getCategories } from '../../api/baseData'
import { STATUS_MAP, ASSET_TYPES } from '../../utils/constants'
import LabelDialog from '../../components/assets/LabelDialog.vue'

const loading = ref(false)
const tableData = ref([])
const selectedRows = ref([])
const search = reactive({ search: '', status: '', category: null })
const categoryOptions = ref([])
const pagination = reactive({ page: 1, pageSize: 50, total: 0 })

const showImport = ref(false)
const showExport = ref(false)
const importType = ref('')
const uploadFile = ref(null)
const fileList = ref([])
const importResult = ref(null)
const exportFields = ref(['asset_number', 'name', 'asset_type', 'category', 'brand', 'spec_model', 'serial_number', 'status', 'department', 'responsible_person', 'purchase_date'])
const labelDialogRef = ref(null)

const buildParams = () => {
  const params = { page: pagination.page, page_size: pagination.pageSize }
  if (search.search) params.search = search.search
  if (search.status) params.status = search.status
  if (search.category) params.category = search.category
  return params
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getAssets(buildParams())
    tableData.value = res.data.results
    pagination.total = res.data.count
  } finally {
    loading.value = false
  }
}

const doSearch = () => { pagination.page = 1; fetchData() }
const resetSearch = () => { search.search = ''; search.status = ''; search.category = null; pagination.page = 1; fetchData() }
const handleSelectionChange = (rows) => { selectedRows.value = rows }

const handleRowCommand = async (cmd, row) => {
  if (cmd === 'delete') {
    try {
      await ElMessageBox.confirm('确定删除该资产吗？', '确认删除', { type: 'warning' })
      await deleteAsset(row.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch { /* cancelled */ }
  } else if (cmd === 'label') {
    labelDialogRef.value.open(row)
  }
}

const handleFileChange = (file) => { uploadFile.value = file.raw || file }

const handleImport = async () => {
  if (!uploadFile.value) return
  const fd = new FormData()
  fd.append('file', uploadFile.value)
  fd.append('asset_type', importType.value)
  try {
    const res = await importAssets(fd)
    importResult.value = res.data
    if (res.data.success_count) { fetchData(); ElMessage.success(`成功导入 ${res.data.success_count} 条`) }
  } catch { ElMessage.error('导入失败') }
}

const handleExport = async () => {
  try {
    const params = buildParams()
    params.fields = exportFields.value.join(',')
    const res = await exportAssets(params)
    const blob = new Blob([res.data])
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'asset_export.xlsx'; a.click()
    URL.revokeObjectURL(url)
    showExport.value = false
  } catch { ElMessage.error('导出失败') }
}

const handleDownloadTemplate = async () => {
  try {
    const res = await downloadTemplate('')
    const blob = new Blob([res.data])
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = 'asset_import_template.xlsx'; a.click()
    URL.revokeObjectURL(url)
  } catch { ElMessage.error('下载失败') }
}

const handleBatchDelete = async () => {
    const count = selectedRows.value.length
    try {
      await ElMessageBox.confirm(
        `确定要删除选中的 ${count} 条资产吗？此操作不可恢复！`,
        '批量删除确认',
        { type: 'warning', confirmButtonText: '确定删除', cancelButtonText: '取消' }
      )
      const ids = selectedRows.value.map(r => r.id)
      const res = await batchDeleteAssets(ids)
      ElMessage.success(res.data.message || `成功删除 ${res.data.deleted} 条资产`)
      fetchData()
    } catch { /* cancelled */ }
  }


const handleBatchPrint = () => {
  if (selectedRows.value.length) {
    labelDialogRef.value.openBatch(selectedRows.value)
  }
}

onMounted(async () => {
  const res = await getCategories()
  categoryOptions.value = res.data.results || res.data
  fetchData()
})
</script>

<style scoped>
.search-card, .action-card { margin-bottom: 16px; }
</style>
