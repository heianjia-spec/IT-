<template>
  <div>
    <el-row :gutter="16">
      <!-- Left: Editor -->
      <el-col :span="16">
        <el-card header="邮件模板编辑" v-loading="loading">
          <el-form :model="form" label-width="100px">
            <el-form-item label="邮件主题">
              <el-input v-model="form.subject" />
            </el-form-item>
            <el-form-item label="邮件正文（HTML）">
              <el-input v-model="form.body" type="textarea" :rows="16" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSave">保存模板</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Right: Variables + Preview -->
      <el-col :span="8">
        <!-- Available Variables -->
        <el-card header="可用变量" style="margin-bottom:16px">
          <p class="var-hint">在模板中插入以下变量，发送时会自动替换为实际值：</p>
          <el-tag
            v-for="v in variables"
            :key="v.name"
            style="margin:4px;cursor:pointer"
            @click="insertVar(v.name)"
          >
            {{ v.name }}
          </el-tag>
        </el-card>

        <!-- Preview -->
        <el-card header="效果预览">
          <div class="preview-box">
            <div class="preview-subject">{{ previewSubject }}</div>
            <div class="preview-body" v-html="previewBody" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getEmailTemplate, saveEmailTemplate } from '../../api/alerts'

const loading = ref(false)

const variables = [
  { name: '{{asset_number}}' },
  { name: '{{asset_name}}' },
  { name: '{{asset_type}}' },
  { name: '{{event_type}}' },
  { name: '{{status}}' },
  { name: '{{department}}' },
  { name: '{{responsible_person}}' },
  { name: '{{detail}}' },
  { name: '{{datetime}}' },
]

const form = reactive({ subject: '', body: '' })

const previewVars = {
  '{{asset_number}}': 'IT-20260612-0001',
  '{{asset_name}}': 'Dell PowerEdge R750',
  '{{asset_type}}': '服务器',
  '{{event_type}}': '维保到期',
  '{{status}}': '在用',
  '{{department}}': '技术部',
  '{{responsible_person}}': '张三',
  '{{detail}}': '该资产维保将于30天后到期',
  '{{datetime}}': '2026-06-12 14:30:00',
}

const previewSubject = computed(() => {
  let s = form.subject || '（无主题）'
  for (const [k, v] of Object.entries(previewVars)) { s = s.replace(k, v) }
  return s
})

const previewBody = computed(() => {
  let b = form.body || '<p>（无正文）</p>'
  for (const [k, v] of Object.entries(previewVars)) { b = b.replace(k, v) }
  return b
})

const insertVar = (name) => {
  form.body += name
}

const handleSave = async () => {
  try {
    await saveEmailTemplate({ subject: form.subject, body: form.body })
    ElMessage.success('模板保存成功')
  } catch { ElMessage.error('保存失败') }
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await getEmailTemplate()
    if (res.data.id) Object.assign(form, res.data)
  } catch { /* use defaults */ }
  finally { loading.value = false }
})
</script>

<style scoped>
.var-hint { font-size: 13px; color: #909399; margin-bottom: 8px; }
.preview-box { border: 1px solid #e4e7ed; padding: 16px; border-radius: 4px; background: #fafafa; }
.preview-subject { font-size: 16px; font-weight: 600; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #e4e7ed; }
.preview-body { font-size: 14px; }
</style>
