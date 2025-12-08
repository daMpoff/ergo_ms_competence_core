import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useCompetencesList } from './useCompetences.js'

export function useCompetencesListPage() {
  const router = useRouter()
  const toast = useToast()

  const search = ref('')
  const level = ref('')
  const viewMode = ref('table')
  const sortBy = ref('popularity_desc')
  const onlyCore = ref(false)

  const showDesigner = ref(false)
  const draft = ref(createEmptyDraft())

  const { items, loading, error, fetchCompetences } = useCompetencesList()

  const stats = computed(() => {
    const list = items.value || []
    const total = list.length
    const core = list.filter((c) => c.is_core).length
    const avgPopularity = total
      ? Math.round(list.reduce((sum, it) => sum + (it.popularity ?? 0), 0) / total)
      : 0
    const avgRelevance = total
      ? (list.reduce((sum, it) => sum + (it.relevance ?? 0), 0) / total).toFixed(2)
      : '0.00'
    return { total, core, avgPopularity, avgRelevance }
  })

  const displayedItems = computed(() => {
    let list = [...(items.value || [])]

    if (onlyCore.value) {
      // В режиме T‑shaped показываем только узконаправленные компетенции
      list = list.filter((item) => !item.is_core)
    }

    switch (sortBy.value) {
      case 'name_asc':
        list.sort((a, b) => (a.name || '').localeCompare(b.name || '', 'ru-RU'))
        break
      case 'name_desc':
        list.sort((a, b) => (b.name || '').localeCompare(a.name || '', 'ru-RU'))
        break
      case 'relevance_desc':
        list.sort((a, b) => (b.relevance ?? 0) - (a.relevance ?? 0))
        break
      case 'popularity_asc':
        list.sort((a, b) => (a.popularity ?? 0) - (b.popularity ?? 0))
        break
      case 'popularity_desc':
      default:
        list.sort((a, b) => (b.popularity ?? 0) - (a.popularity ?? 0))
        break
    }

    return list
  })

  const levelOptions = [
    { label: 'Все уровни', value: '' },
    { label: 'Junior', value: 'JUNIOR' },
    { label: 'Middle', value: 'MIDDLE' },
    { label: 'Senior', value: 'SENIOR' },
    { label: 'Expert', value: 'EXPERT' },
  ]

  const reload = () => {
    const params = {}
    if (search.value) {
      params.search = search.value
    }
    if (level.value) {
      params.level = level.value
    }
    fetchCompetences(params)
  }

  const resetFilters = () => {
    search.value = ''
    level.value = ''
    sortBy.value = 'popularity_desc'
    onlyCore.value = false
    reload()
  }

  const openDetail = (id) => {
    if (!id) {
      return
    }
    router.push({ name: 'CompetenceCoreCompetenceDetail', params: { id } })
  }

  function createEmptyDraft() {
    return {
      name: '',
      description: '',
      level: 'MIDDLE',
      is_core: false,
      tagsInput: '',
      popularity: 70,
      relevance: 0.8,
    }
  }

  const resetDraft = () => {
    draft.value = createEmptyDraft()
  }

  const toggleDesigner = () => {
    showDesigner.value = !showDesigner.value
  }

  const canSaveDraft = computed(() => {
    return !!draft.value.name && !!draft.value.description
  })

  const saveDraft = () => {
    if (!canSaveDraft.value) {
      toast.warning('Заполните название и описание компетенции')
      return
    }

    const list = items.value || []
    const nextId = (list.reduce((maxId, it) => Math.max(maxId, Number(it.id) || 0), 0) || 0) + 1

    const tags = draft.value.tagsInput
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean)

    const newCompetence = {
      id: nextId,
      name: draft.value.name,
      description: draft.value.description,
      level_display: mapLevelToDisplay(draft.value.level),
      is_core: !!draft.value.is_core,
      popularity: Number(draft.value.popularity) || 0,
      relevance: Number(draft.value.relevance) || 0,
      tags,
    }

    items.value = [newCompetence, ...list]

    toast.success('Компетенция добавлена (демо-режим, без сохранения в БД)')
    resetDraft()
    showDesigner.value = false
  }

  const mapLevelToDisplay = (value) => {
    switch (value) {
      case 'JUNIOR':
        return 'Junior'
      case 'MIDDLE':
        return 'Middle'
      case 'SENIOR':
        return 'Senior'
      case 'EXPERT':
        return 'Expert'
      default:
        return value || ''
    }
  }

  onMounted(() => {
    reload()
  })

  return {
    search,
    level,
    viewMode,
    sortBy,
    onlyCore,
    items,
    displayedItems,
    loading,
    error,
    stats,
    levelOptions,
    reload,
    resetFilters,
    openDetail,
    showDesigner,
    draft,
    toggleDesigner,
    resetDraft,
    canSaveDraft,
    saveDraft,
  }
}


