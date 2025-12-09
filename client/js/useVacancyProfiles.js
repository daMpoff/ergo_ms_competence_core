import { ref } from 'vue'
import { apiClient } from '@/js/api/manager'
import { endpoints } from '@/js/api/endpoints'

export function useVacancyProfilesList() {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  const mockProfiles = [
    {
      id: 201,
      vacancy_title: 'Backend Developer (Python)',
      vacancy_source: 'HeadHunter',
      competences_count: 12,
      created_at: '2025-01-15T10:00:00Z',
      location: 'Москва',
      salary: '250–320k ₽',
      tags: ['Python', 'Django', 'REST', 'PostgreSQL', 'Celery', 'Docker'],
    },
    {
      id: 202,
      vacancy_title: 'Data Engineer',
      vacancy_source: 'Habr Career',
      competences_count: 11,
      created_at: '2025-02-02T12:30:00Z',
      location: 'Санкт-Петербург',
      salary: '270–360k ₽',
      tags: ['ETL', 'Kafka', 'Airflow', 'DWH', 'dbt', 'Spark'],
    },
    {
      id: 203,
      vacancy_title: 'Frontend Vue Developer',
      vacancy_source: 'Internal',
      competences_count: 9,
      created_at: '2025-02-10T08:15:00Z',
      location: 'Удалённо',
      salary: '220–300k ₽',
      tags: ['Vue', 'TypeScript', 'SPA', 'SSR', 'Design System'],
    },
    {
      id: 204,
      vacancy_title: 'DevOps / SRE Engineer',
      vacancy_source: 'HeadHunter',
      competences_count: 10,
      created_at: '2025-02-20T09:45:00Z',
      location: 'Москва',
      salary: '300–380k ₽',
      tags: ['Kubernetes', 'Docker', 'CI/CD', 'Terraform', 'Monitoring'],
    },
    {
      id: 205,
      vacancy_title: 'Системный аналитик',
      vacancy_source: 'Habr Career',
      competences_count: 8,
      created_at: '2025-02-25T14:10:00Z',
      location: 'Удалённо',
      salary: '200–260k ₽',
      tags: ['BPMN', 'UML', 'BRD', 'SQL'],
    },
  ]

  const fetchProfiles = async (params = {}) => {
    loading.value = true
    error.value = ''
    try {
      const resp = await apiClient.get(endpoints.competenceCore.vacancyProfilesList, params)
      const data = resp.data
      const results = Array.isArray(data) ? data : data.results ?? []
      if (!results || results.length === 0) {
        // Если API вернул пустой список – используем шаблонные данные,
        // чтобы витрина профилей вакансий всегда была наполнена.
        items.value = mockProfiles
      } else {
        items.value = results
      }
    } catch (e) {
      console.error('Ошибка загрузки профилей вакансий', e)
      // Заглушка: условные данные для работы без БД
      items.value = mockProfiles
      error.value = ''
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

  const mockProfile = {
    id: 201,
    vacancy_title: 'Backend Developer (Python)',
    vacancy_source: 'HeadHunter',
    location: 'Москва',
    salary: '250–300k ₽',
    tags: ['Python', 'Django', 'REST', 'PostgreSQL'],
    vacancy_info: {
      title: 'Backend Developer (Python)',
      company: 'ACME Corp',
      city: 'Москва',
      url: 'https://example.com/vacancy/201',
    },
  }

  const mockCompetences = [
    { id: 301, competence_name: 'Backend разработка', priority: 1, required_level_display: 'Senior', is_mandatory: true, weight: 0.18 },
    { id: 302, competence_name: 'Проектирование API', priority: 2, required_level_display: 'Senior', is_mandatory: true, weight: 0.16 },
    { id: 303, competence_name: 'Работа с реляционными БД', priority: 3, required_level_display: 'Middle', is_mandatory: true, weight: 0.14 },
    { id: 304, competence_name: 'Очереди и асинхронность', priority: 4, required_level_display: 'Middle', is_mandatory: true, weight: 0.12 },
    { id: 305, competence_name: 'Observability и логирование', priority: 5, required_level_display: 'Middle', is_mandatory: false, weight: 0.1 },
    { id: 306, competence_name: 'Оптимизация производительности', priority: 6, required_level_display: 'Senior', is_mandatory: false, weight: 0.1 },
    { id: 307, competence_name: 'Контейнеризация и CI/CD', priority: 7, required_level_display: 'Middle', is_mandatory: false, weight: 0.1 },
    { id: 308, competence_name: 'Безопасность приложений', priority: 8, required_level_display: 'Middle', is_mandatory: false, weight: 0.1 },
  ]

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
      // Заглушка: условные данные
      profile.value = { ...mockProfile, id: id || mockProfile.id }
      competences.value = mockCompetences
      error.value = ''
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


