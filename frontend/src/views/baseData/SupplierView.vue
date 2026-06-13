<template>
  <CrudPage title="供应商管理" :columns="columns" :fetch="fetch" :save="save" :del="del" :formFields="formFields" />
</template>

<script setup>
import { getSuppliers, createSupplier, updateSupplier, deleteSupplier } from '../../api/baseData'
import CrudPage from './CrudPage.vue'

const columns = [
  { prop: 'name', label: '名称', width: 180 },
  { prop: 'code', label: '编码', width: 120 },
  { prop: 'contact_person', label: '联系人', width: 100 },
  { prop: 'contact_phone', label: '电话', width: 140 },
]

const formFields = [
  { prop: 'name', label: '名称' },
  { prop: 'code', label: '编码' },
  { prop: 'contact_person', label: '联系人' },
  { prop: 'contact_phone', label: '联系电话' },
  { prop: 'address', label: '地址', type: 'textarea' },
]

const fetch = getSuppliers
const save = (isEdit, id, data) => isEdit ? updateSupplier(id, data) : createSupplier(data)
const del = deleteSupplier
</script>
