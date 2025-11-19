import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'

export function useVacancyProfilesList() {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  const fetchProfiles = async (params = {}) => {
    loading.value = true
    error.value = ''
    try {
      const resp = await apiClient.get(endpoints.competenceCore.vacancyProfilesList, params)
      const data = resp.data
      const results = Array.isArray(data) ? data : data.results ?? []
      items.value = results
    } catch (e) {
      console.error('Ошибка загрузки профилей вакансий', e)
      error.value = 'Ошибка загрузки профилей вакансий'
      items.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    fetchProfiles,
  }
}

export function useVacancyProfileDetail() {
  const profile = ref(null)
  const competences = ref([])
  const loading = ref(false)
  const error = ref('')

  const fetchProfile = async (id) => {
    if (!id) return
    loading.value = true
    error.value = ''
    try {
      const detailEndpoint = endpoints.competenceCore.vacancyProfileDetail(id)
      const resp = await apiClient.get(detailEndpoint)
      profile.value = resp.data

      const compsEndpoint = endpoints.competenceCore.vacancyProfileCompetences(id)
      const compsResp = await apiClient.get(compsEndpoint)
      const data = compsResp.data
      competences.value = Array.isArray(data) ? data : data.results ?? []
    } catch (e) {
      console.error('Ошибка загрузки профиля вакансии', e)
      error.value = 'Ошибка загрузки профиля вакансии'
      profile.value = null
      competences.value = []
    } finally {
      loading.value = false
    }
  }

  return {
    profile,
    competences,
    loading,
    error,
    fetchProfile,
  }
}


