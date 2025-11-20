<template>
  <div class="container py-4">
    <TechnologyToolbar
      :search-input="searchInput"
      :sort-by="sortBy"
      :sort-dir="sortDir"
      :view-mode="viewMode"
      :page-size="pageSize"
      :page-size-options="pageSizeOptions"
      :filtered-count="filteredCount"
      :total-count="totalCount"
      :technologies-word="technologiesWord"
      :found-word="foundWord"
      @update:search-input="searchInput = $event"
      @update:sort-by="sortBy = $event"
      @update:view-mode="viewMode = $event"
      @update:page-size="pageSize = $event"
      @toggle-sort-dir="toggleSortDir"
      @open-create-technology="openCreateTechnology"
      @open-clear-dialog="openClearTechnologiesDialog"
      @open-init-dialog="openInitTechnologiesDialog"
    />

    <TechnologyFilters
      :category="category"
      :categories="categories"
      :show-synonyms-hint="showSynonymsHint"
      @set-category="setCategory"
    />

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

      <TechnologyTableView
        v-else-if="viewMode === 'table'"
        :items="paginatedItems"
        :expanded-id="expandedId"
        :aliases-by-id="aliasesById"
        :aliases-loading="aliasesLoading"
        :aliases-error="aliasesError"
        :children-by-id="childrenById"
        :children-loading="childrenLoading"
        :children-error="childrenError"
        :category-icon="categoryIcon"
        :category-icon-class="categoryIconClass"
        :popularity-percent="popularityPercent"
        @toggle-expanded="toggleExpanded"
      />

      <TechnologyCardsView
        v-else
        :items="paginatedItems"
        :expanded-id="expandedId"
        :aliases-by-id="aliasesById"
        :aliases-loading="aliasesLoading"
        :aliases-error="aliasesError"
        :children-by-id="childrenById"
        :children-loading="childrenLoading"
        :children-error="childrenError"
        :category-icon="categoryIcon"
        :category-icon-class="categoryIconClass"
        :popularity-percent="popularityPercent"
        @toggle-expanded="toggleExpanded"
      />

      <TechnologyPagination
        :page="page"
        :total-pages="totalPages"
        :page-numbers="pageNumbers"
        @update:page="page = $event"
      />
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
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import TechnologyCreateModal from './TechnologyCreateModal.vue'
import TechnologyToolbar from './components/TechnologyToolbar.vue'
import TechnologyFilters from './components/TechnologyFilters.vue'
import TechnologyTableView from './components/TechnologyTableView.vue'
import TechnologyCardsView from './components/TechnologyCardsView.vue'
import TechnologyPagination from './components/TechnologyPagination.vue'
import { useTechnologiesListPage } from '../js/useTechnologiesListPage.js'
import { useTechnologiesMaintenance } from '../js/useTechnologiesMaintenance.js'

const {
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

<style src="../scss/TechnologiesListPage.scss"></style>
