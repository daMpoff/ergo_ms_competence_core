import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVacancyProfilesList } from './useVacancyProfiles.js'

export function useVacancyProfilesListPage() {
  const router = useRouter()

  const search = ref('')
  const source = ref('')
  const viewMode = ref('table')

  const { items, loading, error, fetchProfiles } = useVacancyProfilesList()

  const stats = computed(() => {
    const list = items.value || []
    const total = list.length
    const sourcesSet = new Set(list.map((i) => i.vacancy_source).filter(Boolean))
    const avgCompetences = total
      ? (
          list.reduce(
            (sum, it) => sum + (Number(it.competences_count) || 0),
            0,
          ) / total
        ).toFixed(1)
      : '0.0'
    const lastUpdatedVal =
      list
        .map((i) => i.created_at)
        .filter(Boolean)
        .sort()
        .slice(-1)[0] || null

    return {
      total,
      sources: sourcesSet.size || '—',
      avgCompetences,
      lastUpdatedRaw: lastUpdatedVal,
      lastUpdatedFormatted: formatDate(lastUpdatedVal),
    }
  })

  const reload = () => {
    const params = {}
    if (search.value) {
      params.search = search.value
    }
    if (source.value) {
      params.vacancy_source = source.value
    }
    fetchProfiles(params)
  }

  const openDetail = (id) => {
    if (!id) {
      return
    }
    router.push({ name: 'CompetenceCoreVacancyProfileDetail', params: { id } })
  }

  const formatDate = (value) => {
    if (!value) return '—'
    try {
      const d = new Date(value)
      return d.toLocaleString('ru-RU')
    } catch {
      return value
    }
  }

  onMounted(() => {
    reload()
  })

  return {
    search,
    source,
    viewMode,
    items,
    loading,
    error,
    stats,
    reload,
    openDetail,
    formatDate,
  }
}


