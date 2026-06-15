<template>
  <template v-for="section in templateConfig.sections" :key="section.name">
    <el-card :header="section.name" style="margin-bottom: 16px">
      <el-row :gutter="16">
        <template v-for="field in section.fields" :key="field.key">
          <el-col v-if="isFieldVisible(field)" :span="field.span || 8">
            <!-- text -->
            <el-form-item
              v-if="field.widget === 'text'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-input
                :model-value="modelValue[field.key]"
                :placeholder="field.placeholder || `请输入${field.label}`"
                @update:model-value="(val) => emitUpdate(field.key, val || '')"
              />
            </el-form-item>

            <!-- number -->
            <el-form-item
              v-else-if="field.widget === 'number'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-input-number
                :model-value="modelValue[field.key]"
                :min="0"
                :placeholder="field.placeholder"
                style="width: 100%"
                @update:model-value="(val) => emitUpdate(field.key, val)"
              />
            </el-form-item>

            <!-- date -->
            <el-form-item
              v-else-if="field.widget === 'date'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-date-picker
                :model-value="modelValue[field.key]"
                type="date"
                :placeholder="field.placeholder || '选择日期'"
                style="width: 100%"
                value-format="YYYY-MM-DD"
                @update:model-value="(val) => emitUpdate(field.key, val)"
              />
            </el-form-item>

            <!-- select -->
            <el-form-item
              v-else-if="field.widget === 'select'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-select
                :model-value="modelValue[field.key]"
                :placeholder="field.placeholder || `请选择${field.label}`"
                clearable
                style="width: 100%"
                @update:model-value="(val) => emitUpdate(field.key, val || '')"
              >
                <el-option
                  v-for="opt in field.options"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <!-- switch -->
            <el-form-item
              v-else-if="field.widget === 'switch'"
              :label="field.label"
              :prop="field.key"
            >
              <el-switch
                :model-value="modelValue[field.key]"
                @update:model-value="(val) => emitUpdate(field.key, val)"
              />
            </el-form-item>

            <!-- textarea -->
            <el-form-item
              v-else-if="field.widget === 'textarea'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-input
                :model-value="modelValue[field.key]"
                type="textarea"
                :rows="field.rows || 2"
                :placeholder="field.placeholder || `请输入${field.label}`"
                @update:model-value="(val) => emitUpdate(field.key, val || '')"
              />
            </el-form-item>

            <!-- tree_select -->
            <el-form-item
              v-else-if="field.widget === 'tree_select'"
              :label="field.label"
              :required="field.required"
              :prop="field.key"
            >
              <el-tree-select
                :model-value="modelValue[field.key]"
                :data="getDataSource(field.data_source)"
                :props="{ value: 'id', label: 'name' }"
                :placeholder="field.placeholder || `请选择${field.label}`"
                check-strictly
                clearable
                style="width: 100%"
                @update:model-value="(val) => emitUpdate(field.key, val)"
              />
            </el-form-item>

            <!-- fallback: treat as text -->
            <el-form-item
              v-else
              :label="field.label"
              :prop="field.key"
            >
              <el-input
                :model-value="modelValue[field.key]"
                :placeholder="field.placeholder"
                @update:model-value="(val) => emitUpdate(field.key, val || '')"
              />
            </el-form-item>
          </el-col>
        </template>
      </el-row>
    </el-card>
  </template>
</template>

<script setup>
import { toRefs } from 'vue'

const props = defineProps({
  /** Merged template config from API */
  templateConfig: { type: Object, default: () => ({ sections: [] }) },
  /** Form data object (v-model) */
  modelValue: { type: Object, default: () => ({}) },
  /** Context for conditional visibility (e.g. { asset_type, status }) */
  context: { type: Object, default: () => ({}) },
  /** Data sources for tree_select widgets */
  dataSources: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue'])

const { templateConfig, modelValue, context, dataSources } = toRefs(props)

function emitUpdate(key, val) {
  emit('update:modelValue', { ...modelValue.value, [key]: val })
}

function getDataSource(name) {
  if (!name) return []
  return dataSources.value[name] || []
}

function isFieldVisible(field) {
  if (!field.visible_when) return true
  const { field: checkField, operator, value } = field.visible_when

  if (operator === 'eq') {
    return context.value[checkField] === value
  }
  if (operator === 'not_eq') {
    return context.value[checkField] !== value
  }
  if (operator === 'in') {
    return Array.isArray(value) && value.includes(context.value[checkField])
  }
  if (operator === 'not_null') {
    return !!modelValue.value[checkField]
  }
  return true
}
</script>
