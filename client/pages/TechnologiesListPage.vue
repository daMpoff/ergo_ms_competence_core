<template>
  <div class="container py-4">
    <!-- Заголовок и общие контролы фильтрации. -->
    <div
      class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-3 tech-toolbar"
    >
      <div>
        <h2 class="mb-1 d-flex align-items-center gap-2 tech-title">
          <Network :size="26" :stroke-width="1.7" class="tech-title-icon" />
          <span>Карта технологий</span>
        </h2>
        <div class="tech-toolbar-count">
          <span v-if="filteredCount > 0">
            <span class="tech-toolbar-count-main">
              {{ foundWord(filteredCount) }} {{ filteredCount }} {{ technologiesWord(filteredCount) }}
            </span>
            <span class="tech-toolbar-count-total">
              из {{ totalCount }} всего
            </span>
          </span>
          <span v-else>
            Ничего не найдено
          </span>
        </div>
      </div>

      <div class="d-flex flex-wrap align-items-stretch tech-toolbar-controls">
        <div class="tech-toolbar-block tech-toolbar-search">
          <div class="input-group input-group-sm">
            <span class="input-group-text">Поиск</span>
            <input
              v-model="searchInput"
              type="text"
              class="form-control"
              placeholder="Название или описание"
            />
          </div>
        </div>

        <div class="tech-toolbar-block tech-toolbar-sort d-flex flex-wrap align-items-center gap-2">
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
        </div>

        <div class="tech-toolbar-block tech-toolbar-page-size">
          <div class="input-group input-group-sm w-auto">
            <span class="input-group-text">На странице</span>
            <select v-model.number="pageSize" class="form-select form-select-sm">
              <option v-for="size in pageSizeOptions" :key="size" :value="size">
                {{ size }}
              </option>
            </select>
          </div>
        </div>

        <div class="tech-toolbar-block tech-toolbar-view">
          <div class="btn-group btn-group-sm tech-view-toggle" role="group">
            <button
              type="button"
              class="btn tech-view-toggle-btn"
              :class="viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary'"
              @click="viewMode = 'table'"
            >
              <span class="tech-view-toggle-icon">
                <LayoutList :size="16" :stroke-width="1.8" />
              </span>
              <span>Таблица</span>
            </button>
            <button
              type="button"
              class="btn tech-view-toggle-btn"
              :class="viewMode === 'cards' ? 'btn-primary' : 'btn-outline-primary'"
              @click="viewMode = 'cards'"
            >
              <span class="tech-view-toggle-icon">
                <LayoutGrid :size="16" :stroke-width="1.8" />
              </span>
              <span>Карточки</span>
            </button>
          </div>
        </div>

        <div class="tech-toolbar-actions tech-add-button-wrap d-flex flex-wrap gap-2">
          <button
            type="button"
            class="btn btn-sm btn-primary d-inline-flex align-items-center gap-2 tech-add-button"
            @click="openCreateTechnology"
          >
            <span class="tech-add-button-icon">
              <Plus :size="14" :stroke-width="2.2" />
            </span>
            <span class="tech-add-button-label">Добавить технологию</span>
          </button>
          <button
            type="button"
            class="btn btn-sm btn-outline-danger d-inline-flex align-items-center gap-2"
            @click="openClearTechnologiesDialog"
          >
            <span class="d-flex align-items-center">
              <Trash2 :size="14" :stroke-width="2" />
            </span>
            <span class="d-none d-sm-inline">Очистить технологии</span>
          </button>
          <button
            type="button"
            class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-2"
            @click="openInitTechnologiesDialog"
          >
            <span class="d-flex align-items-center">
              <RefreshCcw :size="14" :stroke-width="2" />
            </span>
            <span class="d-none d-sm-inline">Инициализировать (dev)</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Категории как интерактивные "чипы". -->
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
      <Transition name="synonyms-hint">
        <div v-if="showSynonymsHint" class="tech-synonyms-hint mt-2">
          <span class="tech-synonyms-hint-icon">
            <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
              <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5" />
              <line x1="12" y1="10" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
              <circle cx="12" cy="7" r="1" fill="currentColor" />
            </svg>
          </span>
          <span class="tech-synonyms-hint-text">
            Нажмите по строке технологии или по кнопке в карточке для просмотра синонимов
          </span>
        </div>
      </Transition>
    </div>

    <div v-if="loading" class="tech-loading py-5">
      <div class="tech-loading-spinner mb-3"></div>
      <div class="w-100">
        <div v-for="n in 5" :key="n" class="tech-skeleton-row">
          <div class="tech-skeleton tech-skeleton-title"></div>
          <div class="tech-skeleton tech-skeleton-subtitle"></div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="sortedItems.length === 0" class="alert alert-info">
        Технологии не найдены. Попробуйте изменить фильтры.
      </div>

      <!-- Табличное представление технологий. -->
      <div v-else-if="viewMode === 'table'" class="table-responsive">
        <table class="table table-hover align-middle tech-table">
          <thead class="table-light">
            <tr>
              <th class="tech-table-head">Название</th>
              <th class="tech-table-head d-none d-md-table-cell">Категория</th>
              <th class="tech-table-head text-end">Популярность</th>
              <th class="tech-table-head text-end d-none d-md-table-cell">Релевантность</th>
              <th class="tech-table-head text-end d-none d-lg-table-cell">Упоминаний</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="tech in paginatedItems" :key="tech.id">
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
                  <span
                    v-if="tech.category_display"
                    class="badge rounded-pill tech-category-badge"
                  >
                    <span
                      class="tech-category-icon-wrap"
                      :class="categoryIconClass(tech.category)"
                    >
                      <component
                        :is="categoryIcon(tech.category)"
                        :size="12"
                        stroke-width="1.8"
                        class="tech-category-icon"
                      />
                    </span>
                    <span>{{ tech.category_display }}</span>
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
                  <div class="tech-expanded-cell position-relative">
                    <div class="d-flex justify-content-between align-items-start">
                      <div class="tech-section-header">
                        <span class="tech-section-title">Синонимы</span>
                        <span
                          v-if="tech.aliases_count"
                          class="tech-section-count"
                        >
                          ({{ tech.aliases_count }})
                        </span>
                        <span
                          v-if="aliasesLoading[tech.id]"
                          class="tech-section-status text-muted"
                        >
                          Загрузка...
                        </span>
                        <span
                          v-else-if="aliasesError[tech.id]"
                          class="tech-section-status text-danger"
                        >
                          {{ aliasesError[tech.id] }}
                        </span>
                      </div>
                      <button
                        type="button"
                        class="tech-close-btn"
                        @click.stop="toggleExpanded(tech, true)"
                      >
                        <span class="tech-close-btn-icon"></span>
                      </button>
                    </div>

                    <div class="row g-2 align-items-start">
                      <div class="col-12">
                        <div
                          v-if="aliasesById[tech.id]?.length"
                          class="d-flex flex-wrap gap-2"
                        >
                          <span
                            v-for="alias in aliasesById[tech.id]"
                            :key="alias.id"
                            class="tech-alias-badge"
                          >
                            {{ alias.alias }}
                          </span>
                        </div>
                        <div v-else-if="!aliasesLoading[tech.id]" class="text-muted small">
                          Синонимов не найдено.
                        </div>
                      </div>
                      <div class="col-12">
                        <div class="tech-section-header">
                          <span class="tech-section-title">Дочерние технологии</span>
                          <span
                            v-if="tech.child_technologies_count"
                            class="tech-section-count"
                          >
                            ({{ tech.child_technologies_count }})
                          </span>
                        </div>
                        <div v-if="childrenLoading[tech.id]" class="text-muted small">
                          Загрузка...
                        </div>
                        <div v-else-if="childrenError[tech.id]" class="text-danger small">
                          {{ childrenError[tech.id] }}
                        </div>
                        <div
                          v-else-if="childrenById[tech.id]?.length"
                          class="d-flex flex-wrap gap-2"
                        >
                          <span
                            v-for="child in childrenById[tech.id]"
                            :key="child.id"
                            class="tech-child-badge"
                          >
                            {{ child.name }}
                          </span>
                        </div>
                        <div v-else class="tech-section-empty">
                          <span class="tech-section-empty-icon">
                            <svg
                              viewBox="0 0 24 24"
                              width="14"
                              height="14"
                              aria-hidden="true"
                            >
                              <circle
                                cx="12"
                                cy="12"
                                r="9"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="1.5"
                              />
                              <line
                                x1="8"
                                y1="12"
                                x2="16"
                                y2="12"
                                stroke="currentColor"
                                stroke-width="1.5"
                                stroke-linecap="round"
                              />
                            </svg>
                          </span>
                          <span class="tech-section-empty-text">
                            Дочерние технологии отсутствуют
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Представление технологий карточками. -->
      <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
        <div v-for="tech in paginatedItems" :key="tech.id" class="col">
          <div
            class="card shadow-sm border-0 tech-card"
            :class="{ 'border-primary': expandedId === tech.id }"
          >
            <div class="card-body d-flex flex-column">
              <div class="tech-card-header d-flex justify-content-between align-items-start mb-2">
                <div class="me-2 flex-grow-1">
                  <div class="d-flex align-items-center gap-2 mb-1">
                    <div
                      v-if="tech.category"
                      class="tech-card-category-icon"
                      :class="categoryIconClass(tech.category)"
                    >
                      <component
                        :is="categoryIcon(tech.category)"
                        :size="14"
                        stroke-width="1.8"
                      />
                    </div>
                    <h5 class="card-title mb-0 text-truncate" :title="tech.name">
                      {{ tech.name }}
                    </h5>
                  </div>
                  <div v-if="tech.category_display" class="text-muted small mb-1">
                    {{ tech.category_display }}
                  </div>
                  <div
                    class="tech-card-meta text-muted small"
                    v-if="tech.aliases_count || tech.child_technologies_count"
                  >
                    <span v-if="tech.aliases_count">
                      Синонимов: {{ tech.aliases_count }}
                    </span>
                    <span
                      v-if="tech.aliases_count && tech.child_technologies_count"
                      class="mx-1"
                    >
                      •
                    </span>
                    <span v-if="tech.child_technologies_count">
                      Дочерние технологии: {{ tech.child_technologies_count }}
                    </span>
                  </div>
                </div>
                <div class="text-end small text-muted d-none d-lg-block ms-2">
                  <div>Популярность: {{ popularityPercent(tech) }}%</div>
                  <div>Упоминаний: {{ tech.occurrence_count ?? 0 }}</div>
                </div>
              </div>

              <p v-if="tech.description" class="card-text text-muted small mb-3">
                {{ tech.description }}
              </p>

              <div class="mt-auto">
                <div class="d-flex flex-wrap gap-2 mb-2 small">
                  <span class="badge bg-light text-dark">
                    Релевантность: {{ (tech.relevance ?? 0).toFixed(2) }}
                  </span>
                  <span class="badge bg-light text-dark">
                    Упоминаний: {{ tech.occurrence_count ?? 0 }}
                  </span>
                </div>

                <div class="mb-2">
                  <div class="d-flex justify-content-between small">
                    <span class="text-muted">Популярность</span>
                    <span>{{ popularityPercent(tech) }}%</span>
                  </div>
                  <div class="progress" style="height: 4px">
                    <div
                      class="progress-bar bg-primary"
                      role="progressbar"
                      :style="{ width: popularityPercent(tech) + '%' }"
                    ></div>
                  </div>
                </div>

                <button
                  type="button"
                  class="btn btn-sm btn-outline-primary w-100 d-flex align-items-center justify-content-center gap-1"
                  @click.stop="toggleExpanded(tech)"
                >
                  <span v-if="expandedId === tech.id">
                    Скрыть
                  </span>
                  <span v-else>
                    Подробнее
                    <span v-if="tech.aliases_count">
                      ({{ tech.aliases_count }})
                    </span>
                  </span>
                </button>

                <Transition name="tech-expand">
                  <div
                    v-if="expandedId === tech.id"
                    class="mt-2 border-top pt-2"
                  >
                    <div class="d-flex justify-content-between align-items-start">
                      <div class="tech-section-header">
                      <span class="tech-section-title">Синонимы</span>
                      <span
                        v-if="tech.aliases_count"
                        class="tech-section-count"
                      >
                        ({{ tech.aliases_count }})
                      </span>
                      <span
                        v-if="aliasesLoading[tech.id]"
                        class="tech-section-status text-muted"
                      >
                        Загрузка...
                      </span>
                      <span
                        v-else-if="aliasesError[tech.id]"
                        class="tech-section-status text-danger"
                      >
                        {{ aliasesError[tech.id] }}
                      </span>
                    </div>
                  </div>

                    <div class="row g-2 align-items-start">
                      <div class="col-12">
                      <div
                        v-if="aliasesById[tech.id]?.length"
                        class="d-flex flex-wrap gap-2"
                      >
                        <span
                          v-for="alias in aliasesById[tech.id]"
                          :key="alias.id"
                          class="tech-alias-badge"
                        >
                          {{ alias.alias }}
                        </span>
                      </div>
                      <div v-else-if="!aliasesLoading[tech.id]" class="text-muted small">
                        Синонимов не найдено.
                      </div>
                    </div>
                      <div class="col-12">
                        <div class="tech-section-header">
                          <span class="tech-section-title">Дочерние технологии</span>
                          <span
                            v-if="tech.child_technologies_count"
                            class="tech-section-count"
                          >
                            ({{ tech.child_technologies_count }})
                          </span>
                        </div>
                        <div v-if="childrenLoading[tech.id]" class="text-muted small">
                        Загрузка...
                      </div>
                        <div v-else-if="childrenError[tech.id]" class="text-danger small">
                        {{ childrenError[tech.id] }}
                      </div>
                      <div
                        v-else-if="childrenById[tech.id]?.length"
                          class="d-flex flex-wrap gap-2"
                      >
                        <span
                          v-for="child in childrenById[tech.id]"
                          :key="child.id"
                          class="tech-child-badge"
                        >
                          {{ child.name }}
                        </span>
                      </div>
                      <div v-else class="tech-section-empty">
                        <span class="tech-section-empty-icon">
                          <svg
                            viewBox="0 0 24 24"
                            width="14"
                            height="14"
                            aria-hidden="true"
                          >
                            <circle
                              cx="12"
                              cy="12"
                              r="9"
                              fill="none"
                              stroke="currentColor"
                              stroke-width="1.5"
                            />
                            <line
                              x1="8"
                              y1="12"
                              x2="16"
                              y2="12"
                              stroke="currentColor"
                              stroke-width="1.5"
                              stroke-linecap="round"
                            />
                          </svg>
                        </span>
                        <span class="tech-section-empty-text">
                          Дочерние технологии отсутствуют
                        </span>
                      </div>
                    </div>
                  </div>
                  </div>
                </Transition>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Пагинация по списку технологий. -->
      <div
        v-if="totalPages > 1"
        class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-2 mt-3"
      >
        <div class="text-muted small">
          Страница {{ page }} из {{ totalPages }}
        </div>
        <nav aria-label="Пагинация по технологиям">
          <ul class="pagination pagination-sm mb-0">
            <li class="page-item" :class="{ disabled: page === 1 }">
              <button
                class="page-link"
                type="button"
                @click="page > 1 && (page = page - 1)"
              >
                Предыдущая
              </button>
            </li>
            <li
              v-for="p in pageNumbers"
              :key="p"
              class="page-item"
              :class="{ active: p === page, disabled: p === '...' }"
            >
              <button
                class="page-link"
                type="button"
                @click="typeof p === 'number' && (page = p)"
              >
                {{ p }}
              </button>
            </li>
            <li class="page-item" :class="{ disabled: page === totalPages }">
              <button
                class="page-link"
                type="button"
                @click="page < totalPages && (page = page + 1)"
              >
                Следующая
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>

    <TechnologyCreateModal
      v-if="showCreateModal"
      v-model="showCreateModal"
      :categories="categories"
      :existing-technologies="items"
      @created="reload"
    />

    <ConfirmDialog
      :show="maintenanceDialog.show"
      :title="maintenanceDialog.title"
      :message="maintenanceDialog.message"
      :confirm-text="maintenanceDialog.confirmText"
      cancel-text="Отмена"
      :variant="maintenanceDialog.variant"
      :loading="dialogLoading"
      @confirm="handleDialogConfirm"
      @cancel="handleDialogCancel"
      @close="handleDialogCancel"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Trash2, RefreshCcw } from 'lucide-vue-next'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import TechnologyCreateModal from './TechnologyCreateModal.vue'
import { useTechnologiesListPage } from '../js/useTechnologiesListPage.js'
import { useTechnologiesMaintenance } from '../js/useTechnologiesMaintenance.js'

const {
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
  search,
  searchInput,
  category,
  sortBy,
  sortDir,
  viewMode,
  expandedId,
  showSynonymsHint,
  showCreateModal,
  page,
  pageSize,
  pageSizeOptions,
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
} = useTechnologiesListPage()

const maintenanceDialog = ref({
  show: false,
  mode: null,
  title: '',
  message: '',
  confirmText: '',
  variant: 'danger',
})

const { clearing, initializing, clearTechnologies, initTechnologies } =
  useTechnologiesMaintenance({
    onChanged: reload,
  })

const openClearTechnologiesDialog = () => {
  maintenanceDialog.value = {
    show: true,
    mode: 'clear',
    title: 'Очистка технологий',
    message: 'Вы действительно хотите удалить все технологии? Это действие нельзя отменить.',
    confirmText: 'Удалить все',
    variant: 'danger',
  }
}

const openInitTechnologiesDialog = () => {
  maintenanceDialog.value = {
    show: true,
    mode: 'init',
    title: 'Инициализация технологий',
    message: 'Будет выполнена первичная инициализация технологий с очисткой текущих данных. Продолжить?',
    confirmText: 'Инициализировать',
    variant: 'warning',
  }
}

const dialogLoading = computed(() => {
  if (maintenanceDialog.value.mode === 'clear') {
    return clearing.value
  }
  if (maintenanceDialog.value.mode === 'init') {
    return initializing.value
  }
  return false
})

const handleDialogCancel = () => {
  if (dialogLoading.value) {
    return
  }
  maintenanceDialog.value = {
    ...maintenanceDialog.value,
    show: false,
  }
}

const handleDialogConfirm = async () => {
  if (dialogLoading.value) return

  try {
    if (maintenanceDialog.value.mode === 'clear') {
      await clearTechnologies()
    } else if (maintenanceDialog.value.mode === 'init') {
      await initTechnologies({
        clear: true,
        update: true,
        dry_run: false,
      })
    }

    maintenanceDialog.value = {
      ...maintenanceDialog.value,
      show: false,
    }
  } catch {
    // Ошибка уже показана через toast
  }
}
</script>

<style scoped src="../scss/TechnologiesListPage.scss"></style>

 
