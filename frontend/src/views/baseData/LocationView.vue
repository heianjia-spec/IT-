<template>
  <CrudPage title="位置管理" :columns="columns" :fetch="fetch" :save="save" :del="del" :formFields="formFields" />
</template>

<script setup>
import { getLocations, createLocation, updateLocation, deleteLocation } from '../../api/baseData'
import CrudPage from './CrudPage.vue'

const columns = [
  { prop: 'name', label: '名称', width: 150 },
  { prop: 'code', label: '编码', width: 120 },
  { prop: 'location_type_display', label: '类型', width: 100 },
  { prop: 'address', label: '地址' },
]

const formFields = [
  { prop: 'name', label: '名称' },
  { prop: 'code', label: '编码' },
  { prop: 'location_type', label: '类型', type: 'select', options: [{ value: 'server_room', label: '机房' }, { value: 'warehouse', label: '库房' }, { value: 'office', label: '办公室' }, { value: 'other', label: '其他' }] },
  { prop: 'address', label: '地址', type: 'textarea' },
]

const fetch = getLocations
const save = (isEdit, id, data) => isEdit ? updateLocation(id, data) : createLocation(data)
const del = deleteLocation
</script>
