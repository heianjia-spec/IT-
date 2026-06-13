<template>
  <div>
    <el-card header="邮件服务器配置">
      <el-form :model="form" label-width="120px" style="max-width:600px" v-loading="loading">
        <el-form-item label="SMTP服务器"><el-input v-model="form.smtp_host" /></el-form-item>
        <el-form-item label="端口"><el-input-number v-model="form.smtp_port" :min="1" :max="65535" /></el-form-item>
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="发件人邮箱"><el-input v-model="form.sender_email" /></el-form-item>
        <el-form-item label="加密方式">
          <el-radio-group v-model="encryption">
            <el-radio :value="'ssl'">SSL (端口 465)</el-radio>
            <el-radio :value="'tls'">TLS (端口 587)</el-radio>
            <el-radio :value="'none'">无</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="启用"><el-switch v-model="form.is_enabled" /></el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSave">保存配置</el-button>
          <el-button @click="showTest = true" :disabled="!form.smtp_host">发送测试邮件</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Test Email Dialog -->
    <el-dialog v-model="showTest" title="发送测试邮件" width="400px">
      <el-form label-width="100px">
        <el-form-item label="收件人邮箱">
          <el-input v-model="testRecipient" placeholder="请输入收件人邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTest = false">取消</el-button>
        <el-button type="primary" :loading="sending" @click="handleTestSend">发送</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getEmailConfig, updateEmailConfig, sendTestEmail } from '../../api/alerts'

const loading = ref(false)
const sending = ref(false)
const showTest = ref(false)
const testRecipient = ref('')
const encryption = ref('ssl')
const form = reactive({ smtp_host: '', smtp_port: 465, username: '', password: '', use_tls: false, use_ssl: true, sender_email: '', is_enabled: false })

onMounted(async () => {
  loading.value = true
  try {
    const res = await getEmailConfig()
    if (res.data.id) {
      Object.assign(form, res.data)
      if (res.data.use_ssl) encryption.value = 'ssl'
      else if (res.data.use_tls) encryption.value = 'tls'
      else encryption.value = 'none'
    }
  } catch { /* empty config */ }
  finally { loading.value = false }
})

const handleSave = async () => {
  form.use_ssl = encryption.value === 'ssl'
  form.use_tls = encryption.value === 'tls'
  if (form.use_ssl) form.smtp_port = form.smtp_port || 465
  if (form.use_tls) form.smtp_port = form.smtp_port || 587
  try { await updateEmailConfig(form); ElMessage.success('保存成功') } catch { ElMessage.error('保存失败') }
}

const handleTestSend = async () => {
  if (!testRecipient.value) { ElMessage.warning('请输入收件人邮箱'); return }
  sending.value = true
  try {
    const res = await sendTestEmail({ recipient: testRecipient.value })
    ElMessage.success(res.data.message || '发送成功')
    showTest.value = false
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '发送失败')
  } finally { sending.value = false }
}
</script>
