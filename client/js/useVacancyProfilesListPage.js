import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVacancyProfilesList } from './useVacancyProfiles.js'

export function useVacancyProfilesListPage() {
  const router = useRouter()

  const search = ref('')
  const source = ref('')
  const viewMode = ref('table')
  const competenceQuery = ref('')
  const minCompetences = ref('')
  const sortBy = ref('created_desc')
  const trackedIds = ref([])

  const syntheticProfiles = [
    {
      id: 'sx-101',
      vacancy_title: 'Lead Backend Engineer (Python, Async, Data)',
      vacancy_source: 'HeadHunter',
      competences_count: 18,
      tags: ['Python', 'FastAPI', 'Kafka', 'PostgreSQL', 'K8s', 'DDD'],
      location: 'Москва / гибрид',
      salary: 'от 330 000 ₽',
      created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-102',
      vacancy_title: 'Staff DevOps / SRE (Multi-cloud)',
      vacancy_source: 'Habr',
      competences_count: 15,
      tags: ['Terraform', 'AWS', 'GCP', 'Prometheus', 'Service Mesh', 'FinOps'],
      location: 'Удаленно',
      salary: 'от 300 000 ₽',
      created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-103',
      vacancy_title: 'Data Platform Architect',
      vacancy_source: 'LinkedIn',
      competences_count: 19,
      tags: ['Spark', 'Airflow', 'Delta Lake', 'MLOps', 'Data Mesh'],
      location: 'Санкт-Петербург',
      salary: 'от 360 000 ₽',
      created_at: new Date(Date.now() - 9 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-104',
      vacancy_title: 'Senior Frontend Engineer (Vue 3 + SSR)',
      vacancy_source: 'Habr',
      competences_count: 12,
      tags: ['Vue', 'SSR', 'TypeScript', 'Design Systems', 'Microfrontends'],
      location: 'Казань / удаленно',
      salary: 'от 250 000 ₽',
      created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-105',
      vacancy_title: 'ML Engineer (NLP, Retrieval)',
      vacancy_source: 'HeadHunter',
      competences_count: 17,
      tags: ['PyTorch', 'Transformers', 'RAG', 'Vector DB', 'Feature Store'],
      location: 'Новосибирск',
      salary: 'от 320 000 ₽',
      created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-106',
      vacancy_title: 'Product Analyst / Analytics Engineer',
      vacancy_source: 'LinkedIn',
      competences_count: 13,
      tags: ['SQL', 'dbt', 'Amplitude', 'Snowflake', 'Experimentation'],
      location: 'Москва / удаленно',
      salary: 'от 240 000 ₽',
      created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-107',
      vacancy_title: 'Solution Architect (Enterprise Integration)',
      vacancy_source: 'HeadHunter',
      competences_count: 16,
      tags: ['ESB', 'API Gateway', 'Security', 'HA/DR'],
      location: 'Москва',
      salary: 'от 340 000 ₽',
      created_at: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
    },
    {
      id: 'sx-108',
      vacancy_title: 'QA Lead (Automation + Performance)',
      vacancy_source: 'Habr',
      competences_count: 14,
      tags: ['Playwright', 'PyTest', 'JMeter', 'Observability'],
      location: 'Екатеринбург / гибрид',
      salary: 'от 230 000 ₽',
      created_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
    },
  ]

  const { items, loading, error, fetchProfiles } = useVacancyProfilesList()

  const stats = computed(() => {
    const list = [...(items.value || []), ...syntheticProfiles]
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
      tracked: trackedIds.value.length,
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
    if (competenceQuery.value) {
      params.competence = competenceQuery.value
    }
    if (minCompetences.value !== '' && !Number.isNaN(Number(minCompetences.value))) {
      params.min_competences = Number(minCompetences.value)
    }
    fetchProfiles(params)
  }

  const displayedItems = computed(() => {
    let list = [...(items.value || []), ...syntheticProfiles]
    if (competenceQuery.value) {
      const q = competenceQuery.value.toLowerCase()
      list = list.filter((i) => {
        const tags = Array.isArray(i.tags) ? i.tags.join(' ').toLowerCase() : ''
        const title = (i.vacancy_title || '').toLowerCase()
        const location = (i.location || '').toLowerCase()
        return tags.includes(q) || title.includes(q) || location.includes(q)
      })
    }
    if (minCompetences.value !== '' && !Number.isNaN(Number(minCompetences.value))) {
      const minVal = Number(minCompetences.value)
      list = list.filter((i) => (Number(i.competences_count) || 0) >= minVal)
    }

    const sorter = {
      created_desc: (a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0),
      created_asc: (a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0),
      competences_desc: (a, b) => (Number(b.competences_count) || 0) - (Number(a.competences_count) || 0),
      competences_asc: (a, b) => (Number(a.competences_count) || 0) - (Number(b.competences_count) || 0),
      title_asc: (a, b) => (a.vacancy_title || '').localeCompare(b.vacancy_title || ''),
      title_desc: (a, b) => (b.vacancy_title || '').localeCompare(a.vacancy_title || ''),
    }

    const sortFn = sorter[sortBy.value] || sorter.created_desc
    return [...list].sort(sortFn)
  })

  const topSources = computed(() => {
    const counts = new Map()
    ;([...(items.value || []), ...syntheticProfiles]).forEach((i) => {
      if (!i.vacancy_source) return
      counts.set(i.vacancy_source, (counts.get(i.vacancy_source) || 0) + 1)
    })
    return Array.from(counts.entries())
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 4)
  })

  const resetFilters = () => {
    search.value = ''
    source.value = ''
    competenceQuery.value = ''
    minCompetences.value = ''
    sortBy.value = 'created_desc'
    reload()
  }

  const setSourceFilter = (value) => {
    source.value = value
    reload()
  }

  const toggleTrack = (id) => {
    if (!id) return false
    if (trackedIds.value.includes(id)) {
      trackedIds.value = trackedIds.value.filter((val) => val !== id)
      return false
    }
    trackedIds.value = [...trackedIds.value, id]
    return true
  }

  const isTracked = (id) => trackedIds.value.includes(id)

  const isFresh = (profile) => {
    if (!profile?.created_at) return false
    const now = new Date()
    const created = new Date(profile.created_at)
    const diffDays = (now - created) / (1000 * 60 * 60 * 24)
    return diffDays <= 7
  }

  const activeFilters = computed(() => {
    const list = []
    if (search.value) list.push({ key: 'search', label: 'Поиск', value: search.value })
    if (source.value) list.push({ key: 'source', label: 'Источник', value: source.value })
    if (competenceQuery.value) list.push({ key: 'competenceQuery', label: 'Компетенция', value: competenceQuery.value })
    if (minCompetences.value !== '' && !Number.isNaN(Number(minCompetences.value))) {
      list.push({ key: 'minCompetences', label: 'Мин. компетенций', value: minCompetences.value })
    }
    const sortLabels = {
      created_desc: 'Сначала новые',
      created_asc: 'Сначала старые',
      competences_desc: 'Больше компетенций',
      competences_asc: 'Меньше компетенций',
      title_asc: 'Название A–Я',
      title_desc: 'Название Я–А',
    }
    if (sortBy.value && sortBy.value !== 'created_desc') {
      list.push({ key: 'sortBy', label: 'Сортировка', value: sortLabels[sortBy.value] || 'Сортировка' })
    }
    return list
  })

  const clearFilter = (key) => {
    switch (key) {
      case 'search':
        search.value = ''
        break
      case 'source':
        source.value = ''
        break
      case 'competenceQuery':
        competenceQuery.value = ''
        break
      case 'minCompetences':
        minCompetences.value = ''
        break
      case 'sortBy':
        sortBy.value = 'created_desc'
        break
      default:
        break
    }
    reload()
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
    competenceQuery,
    minCompetences,
    sortBy,
    trackedIds,
    items,
    displayedItems,
    topSources,
    loading,
    error,
    stats,
    reload,
    resetFilters,
    setSourceFilter,
    toggleTrack,
    isTracked,
    isFresh,
    activeFilters,
    clearFilter,
    openDetail,
    formatDate,
  }
}


