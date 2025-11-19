import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'

export function useCompetencesList() {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  const fetchCompetences = async (params = {}) => {
    loading.value = true
    error.value = ''
    try {
      const resp = await apiClient.get(endpoints.competenceCore.competencesList, params)
      const data = resp.data
      const results = Array.isArray(data) ? data : data.results ?? []
      items.value = results
    } catch (e) {
      console.error('Ошибка загрузки компетенций', e)
      error.value = 'Ошибка загрузки компетенций'
      items.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    fetchCompetences,
  }
}

export function useCompetenceDetail() {
  const item = ref(null)
  const loading = ref(false)
  const error = ref('')

  const fetchCompetence = async (id) => {
    if (!id) return
    loading.value = true
    error.value = ''
    try {
      const endpoint = endpoints.competenceCore.competenceDetail(id)
      const resp = await apiClient.get(endpoint)
      item.value = resp.data
    } catch (e) {
      console.error('Ошибка загрузки компетенции', e)
      error.value = 'Ошибка загрузки компетенции'
      item.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    item,
    loading,
    error,
    fetchCompetence,
  }
}


