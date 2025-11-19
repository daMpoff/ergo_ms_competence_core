<template>
  <div class="container py-4">
    <!-- Заголовок + общий контроллер -->
    <div
      class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3 gap-2"
    >
      <div>
        <h2 class="mb-1">Технологии</h2>
        <div class="text-muted small">
          {{ filteredCount }} из {{ totalCount }} технологий
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2">
        <div class="input-group input-group-sm" style="min-width: 240px">
          <span class="input-group-text">Поиск</span>
          <input
            v-model="search"
            type="text"
            class="form-control"
            placeholder="Название или описание"
          />
        </div>

        <select v-model="sortBy" class="form-select form-select-sm w-auto">
          <option value="popularity">Популярность</option>
          <option value="occurrence">Упоминания</option>
          <option value="relevance">Релевантность</option>
          <option value="name">Название (А→Я)</option>
        </select>

        <button
          type="button"
          class="btn btn-sm btn-outline-secondary"
          @click="toggleSortDir"
        >
          {{ sortDir === 'desc' ? 'По убыванию' : 'По возрастанию' }}
        </button>

        <div class="btn-group btn-group-sm" role="group">
          <button
            type="button"
            class="btn"
            :class="viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary'"
            @click="viewMode = 'table'"
          >
            Таблица
          </button>
          <button
            type="button"
            class="btn"
            :class="viewMode === 'cards' ? 'btn-primary' : 'btn-outline-primary'"
            @click="viewMode = 'cards'"
          >
            Карточки
          </button>
        </div>
      </div>
    </div>

    <!-- Категории как интерактивные "чипы" -->
    <div class="mb-3">
      <div class="d-flex flex-wrap gap-2">
        <button
          type="button"
          class="btn btn-sm"
          :class="!category ? 'btn-primary' : 'btn-outline-primary'"
          @click="setCategory('')"
        >
          Все категории
        </button>
        <button
          v-for="cat in categories"
          :key="cat.value"
          type="button"
          class="btn btn-sm"
          :class="category === cat.value ? 'btn-primary' : 'btn-outline-primary'"
          @click="setCategory(cat.value)"
        >
          {{ cat.label }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5">
      Загрузка...
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="sortedItems.length === 0" class="alert alert-info">
        Технологии не найдены. Попробуйте изменить фильтры.
      </div>

      <!-- Табличное представление -->
      <div v-else-if="viewMode === 'table'" class="table-responsive">
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Название</th>
              <th class="d-none d-md-table-cell">Категория</th>
              <th class="text-end">Популярность</th>
              <th class="text-end d-none d-md-table-cell">Релевантность</th>
              <th class="text-end d-none d-lg-table-cell">Упоминаний</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="tech in sortedItems" :key="tech.id">
              <tr
                class="tech-row"
                :class="{ 'table-active': expandedId === tech.id }"
                @click="toggleExpanded(tech)"
              >
                <td>
                  <div class="fw-semibold">{{ tech.name }}</div>
                  <div v-if="tech.description" class="text-muted small">
                    {{ tech.description }}
                  </div>
                </td>
                <td class="d-none d-md-table-cell">
                  <span v-if="tech.category_display" class="badge bg-light text-dark">
                    {{ tech.category_display }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex flex-column align-items-end gap-1">
                    <div>{{ tech.popularity }}</div>
                    <div class="progress w-100" style="height: 4px">
                      <div
                        class="progress-bar bg-primary"
                        role="progressbar"
                        :style="{ width: popularityPercent(tech) + '%' }"
                      ></div>
                    </div>
                  </div>
                </td>
                <td class="text-end d-none d-md-table-cell">
                  {{ (tech.relevance ?? 0).toFixed(2) }}
                </td>
                <td class="text-end d-none d-lg-table-cell">
                  {{ tech.occurrence_count }}
                </td>
              </tr>
              <tr v-if="expandedId === tech.id">
                <td colspan="5" class="bg-light">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <strong>Синонимы:</strong>
                      <span v-if="aliasesLoading[tech.id]" class="text-muted ms-2">
                        Загрузка...
                      </span>
                      <span v-else-if="aliasesError[tech.id]" class="text-danger ms-2">
                        {{ aliasesError[tech.id] }}
                      </span>
                    </div>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary"
                      @click.stop="toggleExpanded(tech, true)"
                    >
                      Закрыть
                    </button>
                  </div>

                  <div v-if="aliasesById[tech.id]?.length" class="mt-2 d-flex flex-wrap gap-2">
                    <span
                      v-for="alias in aliasesById[tech.id]"
                      :key="alias.id"
                      class="badge bg-secondary"
                    >
                      {{ alias.alias }}
                    </span>
                  </div>
                  <div v-else-if="!aliasesLoading[tech.id]" class="mt-2 text-muted small">
                    Синонимов не найдено.
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Представление карточками -->
      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
        <div v-for="tech in sortedItems" :key="tech.id" class="col">
          <div
            class="card h-100 shadow-sm border-0 tech-card"
            :class="{ 'border-primary': expandedId === tech.id }"
          >
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title mb-0">{{ tech.name }}</h5>
                <span
                  v-if="tech.category_display"
                  class="badge bg-light text-dark ms-2"
                >
                  {{ tech.category_display }}
                </span>
              </div>

              <p v-if="tech.description" class="card-text text-muted small mb-3">
                {{ tech.description }}
              </p>

              <div class="mt-auto">
                <div class="d-flex justify-content-between mb-1 small">
                  <span class="text-muted">Популярность</span>
                  <span>{{ tech.popularity }}</span>
                </div>
                <div class="progress mb-2" style="height: 4px">
                  <div
                    class="progress-bar bg-primary"
                    role="progressbar"
                    :style="{ width: popularityPercent(tech) + '%' }"
                  ></div>
                </div>

                <div class="d-flex justify-content-between small text-muted mb-2">
                  <span>Релевантность: {{ (tech.relevance ?? 0).toFixed(2) }}</span>
                  <span>Упоминаний: {{ tech.occurrence_count }}</span>
                </div>

                <button
                  type="button"
                  class="btn btn-sm btn-outline-primary w-100"
                  @click.stop="toggleExpanded(tech)"
                >
                  <span v-if="expandedId === tech.id">
                    Скрыть синонимы
                  </span>
                  <span v-else>
                    Показать синонимы
                  </span>
                </button>

                <div
                  v-if="expandedId === tech.id"
                  class="mt-2 border-top pt-2"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <strong class="small">Синонимы:</strong>
                    <span
                      v-if="aliasesLoading[tech.id]"
                      class="text-muted small ms-2"
                    >
                      Загрузка...
                    </span>
                    <span
                      v-else-if="aliasesError[tech.id]"
                      class="text-danger small ms-2"
                    >
                      {{ aliasesError[tech.id] }}
                    </span>
                  </div>

                  <div
                    v-if="aliasesById[tech.id]?.length"
                    class="mt-2 d-flex flex-wrap gap-2"
                  >
                    <span
                      v-for="alias in aliasesById[tech.id]"
                      :key="alias.id"
                      class="badge bg-secondary"
                    >
                      {{ alias.alias }}
                    </span>
                  </div>
                  <div v-else-if="!aliasesLoading[tech.id]" class="mt-2 text-muted small">
                    Синонимов не найдено.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useTechnologiesList } from '../js/useTechnologies.js'

const search = ref('')
const category = ref('')
const sortBy = ref('popularity')
const sortDir = ref('desc')
const viewMode = ref('table')
const expandedId = ref(null)

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

const popularityPercent = (tech) => {
  const maxPop = Math.max(...items.value.map((t) => t.popularity ?? 0), 1)
  const value = tech.popularity ?? 0
  return Math.round((value / maxPop) * 100)
}

const reload = () => {
  const params = {}
  if (category.value) {
    params.category = category.value
  }
  // Поиск и сортировку оставляем на клиенте для максимальной интерактивности
  fetchTechnologies(params)
}

const setCategory = (value) => {
  category.value = value
  expandedId.value = null
  reload()
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

  if (!aliasesById[tech.id] && !aliasesLoading[tech.id]) {
    await fetchAliases(tech.id)
  }
}

onMounted(async () => {
  await fetchCategories()
  await reload()
})
</script>

<style scoped>
.tech-row {
  cursor: pointer;
}

.tech-card {
  transition: box-shadow 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.tech-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.08);
}
</style>

 
