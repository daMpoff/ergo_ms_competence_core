import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'

export function useTechnologiesList() {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')
  const categories = ref([])
  const aliasesById = ref({})
  const aliasesLoading = ref({})
  const aliasesError = ref({})

  const fetchCategories = async () => {
    try {
      const resp = await apiClient.get(endpoints.competenceCore.technologyCategories)
      const data = resp.data
      categories.value = Array.isArray(data) ? data : data.results ?? []
    } catch (e) {
      console.error('Ошибка загрузки категорий технологий', e)
    }
  }

  const fetchTechnologies = async (params = {}) => {
    loading.value = true
    error.value = ''
    try {
      const resp = await apiClient.get(endpoints.competenceCore.technologiesList, params)
      const data = resp.data
      const results = Array.isArray(data) ? data : data.results ?? []
      items.value = results
    } catch (e) {
      console.error('Ошибка загрузки технологий', e)
      error.value = 'Ошибка загрузки технологий'
      items.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    categories,
    loading,
    error,
    fetchCategories,
    fetchTechnologies,
    aliasesById: aliasesById.value,
    aliasesLoading: aliasesLoading.value,
    aliasesError: aliasesError.value,
    async fetchAliases(id) {
      if (!id) return
      // Если уже загружено и нет ошибки - повторно не ходим
      if (aliasesById.value[id] && !aliasesError.value[id]) {
        return
      }
      if (aliasesLoading.value[id]) {
        return
      }

      aliasesLoading.value = { ...aliasesLoading.value, [id]: true }
      aliasesError.value = { ...aliasesError.value, [id]: '' }

      try {
        const endpoint = endpoints.competenceCore.technologyAliases(id)
        const resp = await apiClient.get(endpoint)
        const data = resp.data
        const list = Array.isArray(data) ? data : data.results ?? []
        aliasesById.value = { ...aliasesById.value, [id]: list }
      } catch (e) {
        console.error('Ошибка загрузки синонимов технологии', e)
        aliasesError.value = {
          ...aliasesError.value,
          [id]: 'Ошибка загрузки синонимов',
        }
        aliasesById.value = { ...aliasesById.value, [id]: [] }
      } finally {
        aliasesLoading.value = { ...aliasesLoading.value, [id]: false }
      }
    },
  }
}


