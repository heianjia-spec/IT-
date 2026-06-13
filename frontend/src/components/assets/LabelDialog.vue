<template>
  <el-dialog v-model="visible" title="资产标签设计" width="900px" @close="close">
    <el-row :gutter="20">
      <el-col :span="14">
        <div class="label-preview" :style="previewStyle" ref="printRef">
          <div class="label-content" style="text-align:center;padding:8px">
            <img v-if="showQr" :src="qrDataUrl" style="margin-bottom:6px" :style="{width:qrSize+'px',height:qrSize+'px'}" />
            <div v-for="f in selectedFields" :key="f" :style="{fontSize:f==='asset_number'?'14px':'10px',fontWeight:f==='asset_number'?'700':'400',marginBottom:'2px',wordBreak:'break-all'}">
              {{ getFieldValue(f) }}
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="10">
        <h4>标签设置</h4>
        <el-form label-width="100px" size="small">
          <el-form-item label="标签尺寸">
            <el-select v-model="labelSize" style="width:100%">
              <el-option v-for="s in LABEL_SIZES" :key="s.value" :label="s.label" :value="s.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="显示字段">
            <el-checkbox-group v-model="selectedFields">
              <el-checkbox label="asset_number">资产编号</el-checkbox>
              <el-checkbox label="name">资产名称</el-checkbox>
              <el-checkbox label="spec_model">规格型号</el-checkbox>
              <el-checkbox label="brand">品牌</el-checkbox>
              <el-checkbox label="serial_number">序列号</el-checkbox>
              <el-checkbox label="department_name">使用部门</el-checkbox>
              <el-checkbox label="responsible_person">责任人</el-checkbox>
              <el-checkbox label="location_name">存放位置</el-checkbox>
              <el-checkbox label="status_display">资产状态</el-checkbox>
              <el-checkbox label="purchase_date">购置日期</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="显示二维码">
            <el-switch v-model="showQr" />
          </el-form-item>
          <el-form-item label="二维码大小" v-if="showQr">
            <el-radio-group v-model="qrSize">
              <el-radio :label="60">小</el-radio>
              <el-radio :label="80">中</el-radio>
              <el-radio :label="100">大</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>
        <el-button type="primary" @click="print" style="margin-top:12px;width:100%">打印标签</el-button>
      </el-col>
    </el-row>
  </el-dialog>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import QRCode from 'qrcode'
import { LABEL_SIZES } from '../../utils/constants'

const visible = ref(false)
const assetData = ref(null)
const labelSize = ref('80x50')
const selectedFields = ref(['asset_number', 'name'])
const showQr = ref(true)
const qrSize = ref(60)
const qrDataUrl = ref('')
const printRef = ref(null)

const SIZE_MAP = { '60x40': { w: 226, h: 151 }, '80x50': { w: 302, h: 189 }, '100x70': { w: 378, h: 264 } }

const previewStyle = computed(() => {
  const s = SIZE_MAP[labelSize.value] || SIZE_MAP['80x50']
  return {
    width: s.w + 'px', height: s.h + 'px', border: '1px dashed #dcdfe6',
    margin: '0 auto', transform: 'scale(1)', transformOrigin: 'center top',
    background: '#fff', overflow: 'hidden',
  }
})

const getFieldValue = (f) => {
  if (!assetData.value) return ''
  if (f === 'asset_number') return `[${assetData.value.asset_number}]`
  if (f === 'status_display') return assetData.value.status_display || ''
  if (f === 'purchase_date') return assetData.value.purchase_date || ''
  return assetData.value[f] || '-'
}

const generateQr = async () => {
  if (!assetData.value || !showQr.value) { qrDataUrl.value = ''; return }
  const url = `${window.location.origin}/assets/${assetData.value.id}`
  qrDataUrl.value = await QRCode.toDataURL(url, { width: qrSize.value * 2, margin: 1 })
}

const open = async (asset) => {
  assetData.value = asset
  visible.value = true
  await nextTick()
  await generateQr()
}

const openBatch = async (assets) => {
  // Batch: just use the first for preview, print all
  if (assets.length) {
    assetData.value = assets[0]
    visible.value = true
    await nextTick()
    await generateQr()
  }
}

const print = () => {
  const printWindow = window.open('', '_blank')
  printWindow.document.write('<html><head><style>')
  printWindow.document.write('@page { size: auto; margin: 2mm; }')
  printWindow.document.write('body { font-family: "Microsoft YaHei", sans-serif; margin: 0; }')
  printWindow.document.write('.label { display: inline-block; border: 1px solid #999; margin: 5px; text-align: center; padding: 8px; page-break-inside: avoid; }')
  printWindow.document.write(`.label { width: ${SIZE_MAP[labelSize.value].w}px; height: ${SIZE_MAP[labelSize.value].h}px; }`)
  printWindow.document.write('</style></head><body>')
  printWindow.document.write('<div class="label">')
  printWindow.document.write(printRef.value.innerHTML)
  printWindow.document.write('</div></body></html>')
  printWindow.document.close()
  setTimeout(() => printWindow.print(), 500)
}

const close = () => {
  assetData.value = null
  qrDataUrl.value = ''
}

defineExpose({ open, openBatch })
</script>
