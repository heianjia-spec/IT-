import api from './index'

export function getAssets(params) {
  return api.get('/assets/', { params })
}

export function getAsset(id) {
  return api.get(`/assets/${id}/`)
}

export function createAsset(data) {
  return api.post('/assets/', data)
}

export function updateAsset(id, data) {
  return api.put(`/assets/${id}/`, data)
}

export function deleteAsset(id) {
  return api.delete(`/assets/${id}/`)
}

export function batchDeleteAssets(ids) {
  return api.post('/assets/batch_delete/', { ids })
}

export function getStatusHistory(id) {
  return api.get(`/assets/${id}/status_history/`)
}

export function getQrCode(id) {
  return api.get(`/assets/${id}/qr_code/`, { responseType: 'blob' })
}

export function downloadTemplate(assetType) {
  return api.get('/assets/template/', { params: { asset_type: assetType }, responseType: 'blob' })
}

export function importAssets(formData) {
  return api.post('/assets/import_assets/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
}

export function exportAssets(params) {
  return api.get('/assets/export/', { params, responseType: 'blob' })
}

export function getOperationLogs(params) {
  return api.get('/assets/operation-logs/', { params })
}
