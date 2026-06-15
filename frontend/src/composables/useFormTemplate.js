import { ref, reactive } from 'vue'
import {
  getFormTemplateByCategory,
  getDepartments,
  getLocations,
  getSuppliers,
} from '../api/baseData'

/**
 * Composable for loading form templates and data sources.
 *
 * Usage:
 *   const { templateConfig, loading, dataSources, loadTemplate, loadDataSources } = useFormTemplate()
 *   await loadDataSources()
 *   watch(categoryId, (id) => loadTemplate(id))
 */
export function useFormTemplate() {
  const templateConfig = ref({ sections: [] })
  const loading = ref(false)
  const currentCategoryId = ref(null)

  const dataSources = reactive({
    departments: [],
    locations: [],
    suppliers: [],
  })

  /**
   * Load merged form template for the given category (with tree inheritance).
   */
  async function loadTemplate(categoryId) {
    if (!categoryId) {
      templateConfig.value = { sections: [] }
      currentCategoryId.value = null
      return
    }
    currentCategoryId.value = categoryId
    loading.value = true
    try {
      const res = await getFormTemplateByCategory(categoryId)
      templateConfig.value = res.data.template || { sections: [] }
    } catch {
      // If template not found or error, return empty
      templateConfig.value = { sections: [] }
    } finally {
      loading.value = false
    }
  }

  /**
   * Load tree-select data sources (departments, locations, suppliers).
   */
  async function loadDataSources() {
    try {
      const [dept, loc, sup] = await Promise.all([
        getDepartments(),
        getLocations(),
        getSuppliers(),
      ])
      dataSources.departments = dept.data.results || dept.data || []
      dataSources.locations = loc.data.results || loc.data || []
      dataSources.suppliers = sup.data.results || sup.data || []
    } catch {
      // Silently ignore load failures
    }
  }

  /**
   * Get data source array by name.
   */
  function getDataSource(name) {
    const map = {
      departments: dataSources.departments,
      locations: dataSources.locations,
      suppliers: dataSources.suppliers,
    }
    return map[name] || []
  }

  return {
    templateConfig,
    loading,
    currentCategoryId,
    dataSources,
    loadTemplate,
    loadDataSources,
    getDataSource,
  }
}
