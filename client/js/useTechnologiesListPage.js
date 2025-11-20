import { ref, onMounted, computed, watch } from 'vue'
import {
  Plus,
  Network,
  Code2,
  Layers,
  Library as LibraryIcon,
  Database,
  Server,
  Cloud,
  Wrench,
  LayoutList,
  LayoutGrid,
} from 'lucide-vue-next'
import { useTechnologiesList } from './useTechnologies.js'

export function useTechnologiesListPage() {
  const search = ref('')
  const searchInput = ref('')
  const category = ref('')
  const sortBy = ref('popularity')
  const sortDir = ref('desc')
  const viewMode = ref('table')
  const expandedId = ref(null)
  const showSynonymsHint = ref(true)
  const showCreateModal = ref(false)
  const page = ref(1)
  const pageSize = ref(20)
  const pageSizeOptions = [10, 20, 50, 100]

  let searchDebounceTimeout = null

  const categoryIcon = (value) => {
    switch (value) {
      case 'LANG':
        return Code2
      case 'FRAMEWORK':
        return Layers
      case 'LIBRARY':
        return LibraryIcon
      case 'DB':
        return Database
      case 'PLATFORM':
        return Cloud
      case 'PROTOCOL':
        return Network
      case 'SERVICE':
        return Server
      case 'TOOL':
      default:
        return Wrench
    }
  }

  const categoryIconClass = (value) => {
    switch (value) {
      case 'LANG':
        return 'tech-category-icon-lang'
      case 'FRAMEWORK':
        return 'tech-category-icon-framework'
      case 'LIBRARY':
        return 'tech-category-icon-library'
      case 'DB':
        return 'tech-category-icon-db'
      case 'PLATFORM':
        return 'tech-category-icon-platform'
      case 'PROTOCOL':
        return 'tech-category-icon-protocol'
      case 'SERVICE':
        return 'tech-category-icon-service'
      case 'TOOL':
      default:
        return 'tech-category-icon-tool'
    }
  }

  const {
    items,
    categories,
    loading,
    error,
    fetchCategories,
    fetchTechnologies,
    aliasesById,
    aliasesLoading,
    aliasesError,
    fetchAliases,
    childrenById,
    childrenLoading,
    childrenError,
    fetchChildren,
  } = useTechnologiesList()

  const totalCount = computed(() => items.value.length)

  const filteredItems = computed(() => {
    const term = search.value.trim().toLowerCase()
    return items.value.filter((tech) => {
      const matchesCategory = !category.value || tech.category === category.value
      if (!term) return matchesCategory

      const inName = tech.name?.toLowerCase().includes(term)
      const inDesc = tech.description?.toLowerCase().includes(term)
      return matchesCategory && (inName || inDesc)
    })
  })

  const filteredCount = computed(() => filteredItems.value.length)

  const sortedItems = computed(() => {
    const list = [...filteredItems.value]
    const dir = sortDir.value === 'asc' ? 1 : -1

    return list.sort((a, b) => {
      let av
      let bv

      switch (sortBy.value) {
        case 'name':
          av = (a.name || '').toLowerCase()
          bv = (b.name || '').toLowerCase()
          if (av < bv) return -1 * dir
          if (av > bv) return 1 * dir
          return 0
        case 'occurrence':
          av = a.occurrence_count ?? 0
          bv = b.occurrence_count ?? 0
          break
        case 'relevance':
          av = a.relevance ?? 0
          bv = b.relevance ?? 0
          break
        case 'popularity':
        default:
          av = a.popularity ?? 0
          bv = b.popularity ?? 0
          break
      }

      if (av === bv) {
        const an = (a.name || '').toLowerCase()
        const bn = (b.name || '').toLowerCase()
        if (an < bn) return -1
        if (an > bn) return 1
        return 0
      }

      return av > bv ? dir : -dir
    })
  })

  const totalPages = computed(() => {
    if (filteredCount.value === 0) {
      return 1
    }
    return Math.ceil(filteredCount.value / pageSize.value)
  })

  const pageStart = computed(() => {
    if (filteredCount.value === 0) {
      return 0
    }
    return (page.value - 1) * pageSize.value + 1
  })

  const pageEnd = computed(() => {
    if (filteredCount.value === 0) {
      return 0
    }
    return Math.min(filteredCount.value, page.value * pageSize.value)
  })

  const paginatedItems = computed(() => {
    const start = (page.value - 1) * pageSize.value
    const end = start + pageSize.value
    return sortedItems.value.slice(start, end)
  })

  const pageNumbers = computed(() => {
    const pages = []
    const maxToShow = 7
    const total = totalPages.value

    if (total <= maxToShow) {
      for (let i = 1; i <= total; i += 1) {
        pages.push(i)
      }
      return pages
    }

    const current = page.value
    pages.push(1)

    const start = Math.max(2, current - 2)
    const end = Math.min(total - 1, current + 2)

    if (start > 2) {
      pages.push('...')
    }

    for (let i = start; i <= end; i += 1) {
      pages.push(i)
    }

    if (end < total - 1) {
      pages.push('...')
    }

    pages.push(total)

    return pages
  })

  const technologiesWord = (count) => {
    const n = Math.abs(count) % 100
    const last = n % 10

    if (n > 10 && n < 20) {
      return 'технологий'
    }
    if (last === 1) {
      return 'технология'
    }
    if (last >= 2 && last <= 4) {
      return 'технологии'
    }
    return 'технологий'
  }

  const foundWord = (count) => {
    const n = Math.abs(count) % 100
    const last = n % 10

    if (n > 10 && n < 20) {
      return 'Найдено'
    }
    if (last === 1) {
      return 'Найдена'
    }
    if (last >= 2 && last <= 4) {
      return 'Найдены'
    }
    return 'Найдено'
  }

  // При изменении количества элементов на странице всегда начинаем с первой страницы.
  watch(pageSize, () => {
    page.value = 1
  })

  // Дебаунс для строки поиска.
  watch(
    searchInput,
    (value) => {
      const trimmed = value.trimStart()
      // Небольшой дебаунс, чтобы не пересчитывать на каждый символ.
      if (searchDebounceTimeout !== null) {
        clearTimeout(searchDebounceTimeout)
      }
      searchDebounceTimeout = setTimeout(() => {
        search.value = trimmed
        page.value = 1
      }, 300)
    },
    { flush: 'sync' },
  )

  // При изменении количества отфильтрованных элементов держим текущую страницу в допустимых пределах.
  watch(filteredCount, () => {
    if (page.value > totalPages.value) {
      page.value = totalPages.value
    }
    if (page.value < 1) {
      page.value = 1
    }
  })

  watch([search, category, sortBy, sortDir], () => {
    page.value = 1
    expandedId.value = null
  })

  const maxPopularity = computed(() => {
    let max = 1
    const list = items.value
    for (let i = 0; i < list.length; i += 1) {
      const value = list[i].popularity ?? 0
      if (value > max) {
        max = value
      }
    }
    return max
  })

  const popularityPercent = (tech) => {
    const value = tech.popularity ?? 0
    return Math.round((value / maxPopularity.value) * 100)
  }

  const openCreateTechnology = () => {
    showCreateModal.value = true
  }

  const reload = () => {
    // Все технологии загружаем один раз, фильтрацию по категории и поиску делаем на клиенте.
    fetchTechnologies({})
  }

  const setCategory = (value) => {
    category.value = value
    expandedId.value = null
  }

  const toggleSortDir = () => {
    sortDir.value = sortDir.value === 'desc' ? 'asc' : 'desc'
  }

  const toggleExpanded = async (tech, forceClose = false) => {
    if (forceClose || expandedId.value === tech.id) {
      expandedId.value = null
      return
    }

    expandedId.value = tech.id

    const tasks = []
    if (!aliasesById.value[tech.id] && !aliasesLoading.value[tech.id]) {
      tasks.push(fetchAliases(tech.id))
    }
    if (!childrenById.value?.[tech.id] && !childrenLoading.value?.[tech.id]) {
      tasks.push(fetchChildren(tech.id))
    }
    if (tasks.length) {
      await Promise.all(tasks)
    }
  }

  onMounted(async () => {
    await fetchCategories()
    await reload()

    setTimeout(() => {
      showSynonymsHint.value = false
    }, 5000)
  })

  return {
    // Иконки.
    Plus,
    Network,
    Code2,
    Layers,
    LibraryIcon,
    Database,
    Server,
    Cloud,
    Wrench,
    LayoutList,
    LayoutGrid,
    // Состояние.
    search,
    searchInput,
    category,
    sortBy,
    sortDir,
    viewMode,
    expandedId,
    showSynonymsHint,
    page,
    pageSize,
    pageSizeOptions,
    showCreateModal,
    // Данные и вычисления.
    items,
    categories,
    loading,
    error,
    aliasesById,
    aliasesLoading,
    aliasesError,
    childrenById,
    childrenLoading,
    childrenError,
    totalCount,
    filteredItems,
    filteredCount,
    sortedItems,
    totalPages,
    pageStart,
    pageEnd,
    paginatedItems,
    pageNumbers,
    maxPopularity,
    // Функции.
    technologiesWord,
    foundWord,
    popularityPercent,
    openCreateTechnology,
    reload,
    setCategory,
    toggleSortDir,
    toggleExpanded,
    categoryIcon,
    categoryIconClass,
  }
}
