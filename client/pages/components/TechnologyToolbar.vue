<template>
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
            :value="searchInput"
            type="text"
            class="form-control"
            placeholder="Название или описание"
            @input="$emit('update:searchInput', $event.target.value)"
          />
        </div>
      </div>

      <div class="tech-toolbar-block tech-toolbar-sort d-flex flex-wrap align-items-center gap-2">
        <select :value="sortBy" class="form-select form-select-sm w-auto" @change="$emit('update:sortBy', $event.target.value)">
          <option value="popularity">Популярность</option>
          <option value="occurrence">Упоминания</option>
          <option value="relevance">Релевантность</option>
          <option value="name">Название (А→Я)</option>
        </select>

        <button
          type="button"
          class="btn btn-sm btn-outline-secondary"
          @click="$emit('toggleSortDir')"
        >
          {{ sortDir === 'desc' ? 'По убыванию' : 'По возрастанию' }}
        </button>
      </div>

      <div class="tech-toolbar-block tech-toolbar-page-size">
        <div class="input-group input-group-sm w-auto">
          <span class="input-group-text">На странице</span>
          <select :value="pageSize" class="form-select form-select-sm" @change="$emit('update:pageSize', Number($event.target.value))">
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
            @click="$emit('update:viewMode', 'table')"
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
            @click="$emit('update:viewMode', 'cards')"
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
          @click="$emit('openCreateTechnology')"
        >
          <span class="tech-add-button-icon">
            <Plus :size="14" :stroke-width="2.2" />
          </span>
          <span class="tech-add-button-label">Добавить технологию</span>
        </button>
        <button
          type="button"
          class="btn btn-sm btn-outline-danger d-inline-flex align-items-center gap-2"
          @click="$emit('openClearDialog')"
        >
          <span class="d-flex align-items-center">
            <Trash2 :size="14" :stroke-width="2" />
          </span>
          <span class="d-none d-sm-inline">Очистить технологии</span>
        </button>
        <button
          type="button"
          class="btn btn-sm btn-outline-secondary d-inline-flex align-items-center gap-2"
          @click="$emit('openInitDialog')"
        >
          <span class="d-flex align-items-center">
            <RefreshCcw :size="14" :stroke-width="2" />
          </span>
          <span class="d-none d-sm-inline">Инициализировать (dev)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Network, Plus, LayoutList, LayoutGrid, Trash2, RefreshCcw } from 'lucide-vue-next'

defineProps({
  searchInput: { type: String, required: true },
  sortBy: { type: String, required: true },
  sortDir: { type: String, required: true },
  viewMode: { type: String, required: true },
  pageSize: { type: Number, required: true },
  pageSizeOptions: { type: Array, required: true },
  filteredCount: { type: Number, required: true },
  totalCount: { type: Number, required: true },
  technologiesWord: { type: Function, required: true },
  foundWord: { type: Function, required: true },
})

defineEmits([
  'update:searchInput',
  'update:sortBy',
  'update:viewMode',
  'update:pageSize',
  'toggleSortDir',
  'openCreateTechnology',
  'openClearDialog',
  'openInitDialog',
])
</script>

