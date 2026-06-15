<template>
  <div class="template-editor">
    <el-page-header content="表单模板管理" @back="$router.push('/dashboard')" />

    <el-row :gutter="20" style="margin-top: 20px">
      <!-- Left: Category Tree -->
      <el-col :span="6">
        <el-card header="资产分类" style="height: calc(100vh - 160px); overflow-y: auto">
          <el-tree
            ref="treeRef"
            :data="categoryTree"
            :props="{ value: 'id', label: 'name', children: 'children' }"
            node-key="id"
            highlight-current
            :expand-on-click-node="false"
            @node-click="handleCategoryClick"
          >
            <template #default="{ data }">
              <span class="category-node">
                <span>{{ data.name }}</span>
                <el-tag v-if="hasOwnTemplate(data.id)" size="small" type="success" style="margin-left: 6px">已配置</el-tag>
                <el-tag v-else-if="hasInheritedTemplate(data.id)" size="small" type="info" style="margin-left: 6px">继承</el-tag>
              </span>
            </template>
          </el-tree>
        </el-card>
      </el-col>

      <!-- Right: Template Editor -->
      <el-col :span="18">
        <el-card v-if="!selectedCategory" style="height: calc(100vh - 160px); display: flex; align-items: center; justify-content: center">
          <el-empty description="请从左侧选择一个分类" />
        </el-card>

        <template v-else>
          <!-- Template Header -->
          <el-card style="margin-bottom: 16px">
            <div style="display: flex; align-items: center; justify-content: space-between">
              <div>
                <span style="font-size: 16px; font-weight: 600">分类：{{ selectedCategory.name }}</span>
                <el-tag v-if="!isEditingExisting && hasOwnTemplate(selectedCategory.id)" type="warning" size="small" style="margin-left: 12px">
                  当前使用继承模板（未单独配置）
                </el-tag>
                <el-tag v-else-if="isEditingExisting" type="success" size="small" style="margin-left: 12px">自定义模板</el-tag>
              </div>
              <div>
                <el-button v-if="isEditingExisting" type="danger" plain size="small" @click="handleDeleteTemplate">
                  删除自定义模板（恢复继承）
                </el-button>
                <el-button type="primary" @click="handleSaveTemplate" :loading="saving">
                  {{ isEditingExisting ? '更新模板' : '创建自定义模板' }}
                </el-button>
              </div>
            </div>
            <div v-if="inheritanceChain.length > 1" style="margin-top: 8px; font-size: 12px; color: #909399">
              继承链：<span v-for="(item, idx) in inheritanceChain" :key="idx">
                <template v-if="idx > 0"> → </template>
                <el-tag size="small" :type="item.is_self ? 'warning' : (item.has_template ? 'success' : 'info')">
                  {{ item.category_name }}
                  <template v-if="item.has_template && !item.is_self">(模板)</template>
                </el-tag>
              </span>
            </div>
          </el-card>

          <!-- Sections -->
          <div v-for="(section, secIdx) in editingConfig.sections" :key="secIdx">
            <el-card style="margin-bottom: 12px">
              <template #header>
                <div style="display: flex; align-items: center; justify-content: space-between">
                  <el-input v-model="section.name" placeholder="区块名称" style="width: 200px" size="small" />
                  <div>
                    <el-button size="small" :icon="'Top'" @click="moveSection(secIdx, -1)" :disabled="secIdx === 0">上移</el-button>
                    <el-button size="small" :icon="'Bottom'" @click="moveSection(secIdx, 1)" :disabled="secIdx === editingConfig.sections.length - 1">下移</el-button>
                    <el-button size="small" type="danger" @click="removeSection(secIdx)">删除区块</el-button>
                  </div>
                </div>
              </template>

              <!-- Fields in this section -->
              <el-table :data="section.fields" border size="small">
                <el-table-column prop="label" label="字段标签" width="140" />
                <el-table-column prop="key" label="字段名(key)" width="160" />
                <el-table-column label="控件类型" width="100">
                  <template #default="{ row }">{{ WIDGET_LABELS[row.widget] || row.widget }}</template>
                </el-table-column>
                <el-table-column label="必填" width="60">
                  <template #default="{ row }">
                    <el-tag :type="row.required ? 'danger' : 'info'" size="small">{{ row.required ? '是' : '否' }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="span" label="列宽" width="60" />
                <el-table-column label="条件显示" min-width="140">
                  <template #default="{ row }">
                    <span v-if="row.visible_when" style="font-size: 12px; color: #E6A23C">
                      当 {{ row.visible_when.field }} {{ row.visible_when.operator }} {{ row.visible_when.value }}
                    </span>
                    <span v-else style="color: #909399">-</span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="180" fixed="right">
                  <template #default="{ row, $index }">
                    <el-button link type="primary" size="small" @click="openFieldDialog(secIdx, $index)">编辑</el-button>
                    <el-button link size="small" @click="moveField(secIdx, $index, -1)" :disabled="$index === 0">↑</el-button>
                    <el-button link size="small" @click="moveField(secIdx, $index, 1)" :disabled="$index === section.fields.length - 1">↓</el-button>
                    <el-button link type="danger" size="small" @click="removeField(secIdx, $index)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <div style="margin-top: 12px">
                <el-button size="small" type="primary" plain @click="openFieldDialog(secIdx, -1)">
                  + 添加字段
                </el-button>
              </div>
            </el-card>
          </div>

          <el-button type="primary" plain style="margin-top: 12px" @click="addSection">
            + 添加区块
          </el-button>
        </template>
      </el-col>
    </el-row>

    <!-- Field Edit Dialog -->
    <el-dialog
      v-model="fieldDialogVisible"
      :title="editingFieldIndex >= 0 ? '编辑字段' : '添加字段'"
      width="650px"
      destroy-on-close
    >
      <el-form v-if="editingField" :model="editingField" label-width="100px">
        <el-form-item label="字段名(key)">
          <el-select
            v-if="editingFieldIndex < 0"
            v-model="editingField.key"
            filterable
            allow-create
            placeholder="选择或输入字段名"
            style="width: 100%"
            @change="onFieldKeyChange"
          >
            <el-option
              v-for="f in availableFields"
              :key="f.key"
              :label="`${f.label} (${f.key})`"
              :value="f.key"
            />
          </el-select>
          <el-input v-else v-model="editingField.key" disabled />
        </el-form-item>
        <el-form-item label="字段标签">
          <el-input v-model="editingField.label" />
        </el-form-item>
        <el-form-item label="控件类型">
          <el-select v-model="editingField.widget" style="width: 100%">
            <el-option v-for="(label, val) in WIDGET_LABELS" :key="val" :label="label" :value="val" />
          </el-select>
        </el-form-item>
        <el-form-item label="列宽(span)">
          <el-input-number v-model="editingField.span" :min="6" :max="24" :step="2" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="editingField.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="是否必填">
          <el-switch v-model="editingField.required" />
        </el-form-item>
        <el-form-item label="占位提示">
          <el-input v-model="editingField.placeholder" />
        </el-form-item>
        <el-form-item label="帮助文本">
          <el-input v-model="editingField.help_text" />
        </el-form-item>
        <el-form-item label="选项(select)">
          <span style="font-size: 12px; color: #909399">每行一个，格式：value=label，如 laser=激光</span>
          <el-input
            v-model="optionsText"
            type="textarea"
            :rows="4"
            placeholder="laser=激光&#10;inkjet=喷墨"
          />
        </el-form-item>
        <el-form-item label="条件显示">
          <div style="display: flex; gap: 8px; align-items: center">
            <el-input v-model="editingField.visible_when.field" placeholder="字段名" style="width: 160px" />
            <el-select v-model="editingField.visible_when.operator" placeholder="操作符" style="width: 120px">
              <el-option label="等于(eq)" value="eq" />
              <el-option label="不等于(not_eq)" value="not_eq" />
              <el-option label="包含(in)" value="in" />
              <el-option label="非空(not_null)" value="not_null" />
            </el-select>
            <el-input v-if="!['not_null'].includes(editingField.visible_when.operator)" v-model="editingField.visible_when.value" placeholder="值" style="width: 140px" />
            <el-button link type="danger" size="small" @click="editingField.visible_when = {}">清除</el-button>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="fieldDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmFieldDialog">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  getCategories,
  getFormTemplates,
  getFormTemplateByCategory,
  createFormTemplate,
  updateFormTemplate,
  deleteFormTemplate,
  getFieldRegistry,
} from '../../api/baseData'

const WIDGET_LABELS = {
  text: '文本输入',
  number: '数字输入',
  textarea: '多行文本',
  date: '日期选择',
  select: '下拉选择',
  switch: '开关',
  tree_select: '树形选择',
}

const saving = ref(false)
const categoryTree = ref([])
const selectedCategory = ref(null)
const templates = ref([])
const inheritanceChain = ref([])
const isEditingExisting = ref(false)
const editingTemplateId = ref(null)
const fieldRegistry = ref([])

const editingConfig = reactive({ sections: [] })

// Field dialog state
const fieldDialogVisible = ref(false)
const editingSectionIdx = ref(-1)
const editingFieldIndex = ref(-1)
const editingField = ref(null)
const optionsText = ref('')

const availableFields = computed(() => {
  // Return field registry entries not already in the template
  const usedKeys = new Set()
  for (const sec of editingConfig.sections) {
    for (const f of sec.fields) {
      usedKeys.add(f.key)
    }
  }
  return fieldRegistry.value.filter(f => !usedKeys.has(f.key))
})

function hasOwnTemplate(categoryId) {
  return templates.value.some(t => t.category === categoryId)
}

function hasInheritedTemplate(categoryId) {
  // Check if any ancestor has a template
  const findAncestorWithTemplate = (nodes, targetId, found = new Set()) => {
    for (const node of nodes) {
      if (node.id === targetId) return found.size > 0
      found.add(node.id)
      if (node.children?.length) {
        const result = findAncestorWithTemplate(node.children, targetId, new Set(found))
        if (result !== null) return result
      }
      found.delete(node.id)
    }
    return null
  }
  if (hasOwnTemplate(categoryId)) return true
  // Simple check: template API returns non-empty sections for inheritance
  return false
}

async function loadData() {
  try {
    const catRes = await getCategories()
    categoryTree.value = catRes.data.results || catRes.data
  } catch (e) {
    ElMessage.error('加载分类列表失败')
  }

  try {
    const tplRes = await getFormTemplates()
    templates.value = tplRes.data.results || tplRes.data
  } catch (e) {
    ElMessage.warning('加载模板列表失败')
  }

  try {
    const regRes = await getFieldRegistry()
    fieldRegistry.value = regRes.data.fields || []
    if (fieldRegistry.value.length === 0) {
      ElMessage.warning('字段注册表为空，请检查后端服务')
    }
  } catch (e) {
    ElMessage.error('加载字段注册表失败，可手动输入字段名')
    fieldRegistry.value = []
  }
}

async function handleCategoryClick(node) {
  selectedCategory.value = node
  try {
    const res = await getFormTemplateByCategory(node.id)
    inheritanceChain.value = res.data.inheritance_chain || []

    // Check if this category has its own template
    const ownTemplate = templates.value.find(t => t.category === node.id)
    if (ownTemplate) {
      isEditingExisting.value = true
      editingTemplateId.value = ownTemplate.id
      // Load own config (not merged)
      editingConfig.sections = JSON.parse(JSON.stringify(ownTemplate.config?.sections || []))
    } else {
      isEditingExisting.value = false
      editingTemplateId.value = null
      // Pre-populate with merged template so user sees what's inherited
      editingConfig.sections = JSON.parse(JSON.stringify(res.data.template?.sections || []))
    }
  } catch {
    editingConfig.sections = []
    inheritanceChain.value = []
    isEditingExisting.value = false
  }
}

function addSection() {
  editingConfig.sections.push({
    name: '新区块',
    sort_order: editingConfig.sections.length + 1,
    fields: [],
  })
}

function removeSection(idx) {
  editingConfig.sections.splice(idx, 1)
}

function moveSection(idx, delta) {
  const newIdx = idx + delta
  if (newIdx < 0 || newIdx >= editingConfig.sections.length) return
  const temp = editingConfig.sections[idx]
  editingConfig.sections[idx] = editingConfig.sections[newIdx]
  editingConfig.sections[newIdx] = temp
  // Update sort_order
  editingConfig.sections.forEach((s, i) => (s.sort_order = i + 1))
}

function moveField(secIdx, fieldIdx, delta) {
  const fields = editingConfig.sections[secIdx].fields
  const newIdx = fieldIdx + delta
  if (newIdx < 0 || newIdx >= fields.length) return
  const temp = fields[fieldIdx]
  fields[fieldIdx] = fields[newIdx]
  fields[newIdx] = temp
  fields.forEach((f, i) => (f.sort_order = i + 1))
}

function removeField(secIdx, fieldIdx) {
  editingConfig.sections[secIdx].fields.splice(fieldIdx, 1)
}

function openFieldDialog(secIdx, fieldIdx) {
  editingSectionIdx.value = secIdx
  editingFieldIndex.value = fieldIdx

  if (fieldIdx >= 0) {
    // Edit existing field
    const field = editingConfig.sections[secIdx].fields[fieldIdx]
    editingField.value = JSON.parse(JSON.stringify(field))
    // Ensure visible_when object exists
    if (!editingField.value.visible_when) {
      editingField.value.visible_when = {}
    }
    // Convert options to text
    optionsText.value = (field.options || []).map(o => `${o.value}=${o.label}`).join('\n')
  } else {
    // New field
    editingField.value = {
      key: '',
      label: '',
      widget: 'text',
      required: false,
      sort_order: editingConfig.sections[secIdx].fields.length + 1,
      span: 8,
      placeholder: '',
      help_text: '',
      options: [],
      visible_when: {},
    }
    optionsText.value = ''
  }
  fieldDialogVisible.value = true
}

function onFieldKeyChange(key) {
  const reg = fieldRegistry.value.find(f => f.key === key)
  if (reg) {
    editingField.value.label = reg.label
    editingField.value.widget = reg.widget
    if (reg.options) {
      editingField.value.options = reg.options
      optionsText.value = reg.options.map(o => `${o.value}=${o.label}`).join('\n')
    } else {
      optionsText.value = ''
    }
  } else {
    // 自定义字段：自动填充 label 并重置为文本输入
    if (!editingField.value.label) {
      editingField.value.label = key
    }
    editingField.value.widget = editingField.value.widget || 'text'
    editingField.value.options = []
    optionsText.value = ''
  }
}

function confirmFieldDialog() {
  // Parse options text
  if (optionsText.value.trim()) {
    editingField.value.options = optionsText.value
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        const [value, ...labelParts] = line.split('=')
        return { value: value.trim(), label: labelParts.join('=').trim() || value.trim() }
      })
  } else {
    editingField.value.options = []
  }

  // Clean empty visible_when
  if (!editingField.value.visible_when?.field) {
    editingField.value.visible_when = null
  }

  const secIdx = editingSectionIdx.value
  const fieldIdx = editingFieldIndex.value
  const field = JSON.parse(JSON.stringify(editingField.value))

  if (fieldIdx >= 0) {
    editingConfig.sections[secIdx].fields[fieldIdx] = field
  } else {
    editingConfig.sections[secIdx].fields.push(field)
  }

  fieldDialogVisible.value = false
}

async function handleSaveTemplate() {
  saving.value = true
  try {
    // Clean config: assign sort_orders
    editingConfig.sections.forEach((sec, si) => {
      sec.sort_order = si + 1
      sec.fields.forEach((f, fi) => {
        f.sort_order = fi + 1
      })
    })

    const data = {
      category: selectedCategory.value.id,
      name: `${selectedCategory.value.name}模板`,
      config: { sections: editingConfig.sections },
      is_active: true,
    }

    if (isEditingExisting.value && editingTemplateId.value) {
      await updateFormTemplate(editingTemplateId.value, data)
      ElMessage.success('模板已更新')
    } else {
      const res = await createFormTemplate(data)
      editingTemplateId.value = res.data.id
      isEditingExisting.value = true
      ElMessage.success('模板已创建')
    }

    // Reload templates list
    const tplRes = await getFormTemplates()
    templates.value = tplRes.data.results || tplRes.data
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDeleteTemplate() {
  if (!editingTemplateId.value) return
  try {
    await ElMessageBox.confirm('删除自定义模板后将恢复继承父分类的模板，确定继续？', '确认', {
      type: 'warning',
    })
    await deleteFormTemplate(editingTemplateId.value)
    ElMessage.success('已删除自定义模板，恢复继承')
    // Reload
    const tplRes = await getFormTemplates()
    templates.value = tplRes.data.results || tplRes.data
    // Re-fetch merged template
    if (selectedCategory.value) {
      await handleCategoryClick(selectedCategory.value)
    }
  } catch {
    // Cancelled
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.template-editor {
  min-height: calc(100vh - 100px);
}
.category-node {
  display: flex;
  align-items: center;
  font-size: 14px;
}
</style>
