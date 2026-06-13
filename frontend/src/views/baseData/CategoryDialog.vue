<template>
  <el-dialog :title="isEdit ? '编辑分类' : '新增分类'" v-model="visible" width="500px" @close="close">
    <el-form :model="form" label-width="80px" ref="formRef">
      <el-form-item label="名称" required><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="编码" required><el-input v-model="form.code" /></el-form-item>
      <el-form-item label="上级分类"><el-cascader v-model="form.parent" :options="options" :props="{ value:'id', label:'name', checkStrictly:true, emitPath:false }" placeholder="无（顶级分类）" clearable style="width:100%" /></el-form-item>
      <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
      <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="visible = false">取消</el-button>
      <el-button type="primary" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { createCategory, updateCategory, getCategories } from '../../api/baseData'

const emit = defineEmits(['saved'])
const visible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const options = ref([])

const form = reactive({ name: '', code: '', parent: null, description: '', sort_order: 0 })

const open = async (row) => {
  const res = await getCategories()
  options.value = flatten(res.data.results || res.data)
  if (row) {
    isEdit.value = true
    editId.value = row.id
    Object.assign(form, { name: row.name, code: row.code, parent: row.parent, description: row.description || '', sort_order: row.sort_order || 0 })
  } else {
    isEdit.value = false
    Object.assign(form, { name: '', code: '', parent: null, description: '', sort_order: 0 })
  }
  visible.value = true
}

const flatten = (items) => {
  const result = []
  for (const item of items) {
    result.push({ id: item.id, name: item.name, children: item.children?.length ? flatten(item.children) : undefined })
  }
  return result
}

const handleSave = async () => {
  try {
    if (isEdit.value) { await updateCategory(editId.value, form) } else { await createCategory(form) }
    ElMessage.success('保存成功')
    visible.value = false
    emit('saved')
  } catch (e) { ElMessage.error('保存失败') }
}

const close = () => { visible.value = false }

defineExpose({ open })
</script>
