import api from './index'

export const getCategories = (params) => api.get('/categories/', { params })
export const createCategory = (data) => api.post('/categories/', data)
export const updateCategory = (id, data) => api.put(`/categories/${id}/`, data)
export const deleteCategory = (id) => api.delete(`/categories/${id}/`)

export const getDepartments = (params) => api.get('/departments/', { params })
export const createDepartment = (data) => api.post('/departments/', data)
export const updateDepartment = (id, data) => api.put(`/departments/${id}/`, data)
export const deleteDepartment = (id) => api.delete(`/departments/${id}/`)

export const getLocations = (params) => api.get('/locations/', { params })
export const createLocation = (data) => api.post('/locations/', data)
export const updateLocation = (id, data) => api.put(`/locations/${id}/`, data)
export const deleteLocation = (id) => api.delete(`/locations/${id}/`)

export const getSuppliers = (params) => api.get('/suppliers/', { params })
export const createSupplier = (data) => api.post('/suppliers/', data)
export const updateSupplier = (id, data) => api.put(`/suppliers/${id}/`, data)
export const deleteSupplier = (id) => api.delete(`/suppliers/${id}/`)

// Form template APIs
export const getFormTemplateByCategory = (categoryId) =>
  api.get('/form-templates/by_category/', { params: { category_id: categoryId } })
export const getFormTemplates = (params) => api.get('/form-templates/', { params })
export const getFormTemplate = (id) => api.get(`/form-templates/${id}/`)
export const createFormTemplate = (data) => api.post('/form-templates/', data)
export const updateFormTemplate = (id, data) => api.put(`/form-templates/${id}/`, data)
export const deleteFormTemplate = (id) => api.delete(`/form-templates/${id}/`)
export const getFieldRegistry = () => api.get('/form-templates/field_registry/')
