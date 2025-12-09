<template>
  <div class="container py-4">
    <div class="cc-competence-header d-flex flex-column flex-lg-row align-items-lg-center justify-content-between gap-2 mb-3">
      <div class="d-flex align-items-center gap-2">
        <div class="cc-competence-title-icon d-flex align-items-center justify-content-center">
          <BadgeCheck :size="22" :stroke-width="1.7" />
        </div>
        <div>
          <h2 class="mb-1 d-flex align-items-center gap-2">
            Компетенции
          </h2>
          <div class="cc-competence-header-meta text-muted small d-flex flex-wrap align-items-center gap-2">
            <span class="d-inline-flex align-items-center gap-1">
              <Layers :size="14" /> Всего: {{ stats.total }}
            </span>
            <span class="d-inline-flex align-items-center gap-1">
              <Shield :size="14" /> Базовых: {{ stats.core }}
            </span>
            <span class="d-inline-flex align-items-center gap-1">
              <Flame :size="14" /> Узконаправленных: {{ stats.total - stats.core }}
            </span>
          </div>
        </div>
      </div>
      <div class="d-flex flex-wrap gap-2 justify-content-start justify-content-lg-end">
        <button class="btn btn-sm btn-outline-secondary" type="button" @click="reload">
          Обновить данные
        </button>
        <button class="btn btn-sm btn-danger" type="button" @click="toggleDesigner">
          {{ showDesigner ? 'Скрыть конструктор' : 'Создать компетенцию' }}
        </button>
      </div>
    </div>

    <div class="row g-3 cc-competence-layout">
      <div class="col-12">
        <div class="card shadow-sm border-0 mb-3 cc-competence-filters-card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2 cc-competence-filters-header">
              <div>
                <div class="cc-competence-filters-title d-flex align-items-center gap-1">
                  <Filter :size="16" /> Фильтры и представление
                </div>
                <div class="text-muted small">Настройте витрину компетенций, фильтры применяются мгновенно.</div>
              </div>
              <button
                type="button"
                class="btn btn-link btn-sm text-decoration-none p-0"
                @click="resetFilters"
              >
                Сбросить
              </button>
            </div>

            <div class="row g-2 align-items-end cc-filters-row">
              <div class="col-12">
                <label class="form-label text-muted small mb-1">Поиск</label>
                <div class="input-group cc-search-group">
                  <span class="input-group-text">
                    <Search :size="16" />
                  </span>
                  <input
                    v-model="search"
                    type="text"
                    class="form-control"
                    placeholder="Название, описание или тег"
                    @keyup.enter="reload"
                  />
                </div>
              </div>
            </div>

            <div class="row g-3 align-items-end cc-filters-row cc-filters-row--compact">
              <div class="col-12 col-md-4 col-lg-3">
                <label class="form-label text-muted small mb-1">Уровень</label>
                <select v-model="level" class="form-select" @change="reload">
                  <option
                    v-for="opt in levelOptions"
                    :key="opt.value || 'all'"
                    :value="opt.value"
                  >
                    {{ opt.label }}
                  </option>
                </select>
              </div>
              <div class="col-12 col-md-3 col-lg-2">
                <label class="form-label text-muted small mb-1">Сортировка</label>
                <select v-model="sortBy" class="form-select">
                  <option value="popularity_desc">По популярности (по убыванию)</option>
                  <option value="popularity_asc">По популярности (по возрастанию)</option>
                  <option value="relevance_desc">По релевантности</option>
                  <option value="name_asc">По названию (А–Я)</option>
                  <option value="name_desc">По названию (Я–А)</option>
                </select>
              </div>
              <div class="col-12 col-md-4 col-lg-3 d-flex align-items-center">
                <div class="cc-filter-toggle">
                  <input
                    v-model="onlyCore"
                    class="form-check-input d-none"
                    type="checkbox"
                    tabindex="-1"
                  />
                  <label
                    class="cc-filter-toggle-label"
                    :class="{ 'is-active': onlyCore }"
                    role="button"
                    tabindex="0"
                    @click.prevent="onlyCore = !onlyCore"
                    @keydown.enter.prevent="onlyCore = !onlyCore"
                    @keydown.space.prevent="onlyCore = !onlyCore"
                  >
                    <span class="cc-filter-toggle-dot" :class="{ 'is-active': onlyCore }"></span>
                    Узконаправленные
                  </label>
                </div>
              </div>
              <div class="col-12 col-md-4 col-lg-3 mt-1 mt-lg-0">
                <div class="btn-group w-100" role="group" aria-label="view switch">
                  <button
                    type="button"
                    class="btn btn-sm"
                    :class="viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary'"
                    @click="viewMode = 'table'"
                  >
                    Таблица
                  </button>
                  <button
                    type="button"
                    class="btn btn-sm"
                    :class="viewMode === 'cards' ? 'btn-primary' : 'btn-outline-primary'"
                    @click="viewMode = 'cards'"
                  >
                    Карточки
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row g-3 mb-3">
          <div class="col-6 col-lg-3">
            <div class="card shadow-sm border-0 h-100 cc-competence-kpi-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-1">
                  <div class="text-muted small">Всего компетенций</div>
                  <span class="cc-competence-kpi-icon"><Layers :size="20" /></span>
                </div>
                <div class="h4 mb-0 text-dark">{{ stats.total }} шт.</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="card shadow-sm border-0 h-100 cc-competence-kpi-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-1">
                  <div class="text-dark small fw-semibold">Базовых</div>
                  <span class="cc-competence-kpi-icon"><Shield :size="20" /></span>
                </div>
                <div class="h4 mb-0 text-dark">{{ stats.core }} шт.</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="card shadow-sm border-0 h-100 cc-competence-kpi-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-1">
                  <div class="text-dark small fw-semibold">Средняя популярность</div>
                  <span class="cc-competence-kpi-icon"><Sparkle :size="20" /></span>
                </div>
                <div class="h4 mb-0 text-dark">{{ stats.avgPopularity }} %</div>
              </div>
            </div>
          </div>
          <div class="col-6 col-lg-3">
            <div class="card shadow-sm border-0 h-100 cc-competence-kpi-card">
              <div class="card-body">
                <div class="d-flex align-items-center justify-content-between mb-1">
                  <div class="text-dark small fw-semibold">Средняя релевантность</div>
                  <span class="cc-competence-kpi-icon"><Gauge :size="20" /></span>
                </div>
                <div class="h4 mb-0 text-dark">{{ stats.avgRelevance }}</div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="loading" class="text-center py-5 cc-competence-loading">
          Загрузка витрины компетенций...
        </div>

        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-else>
          <div v-if="displayedItems.length === 0" class="alert alert-info">
            Компетенции не найдены. Попробуйте изменить фильтры или создать первую компетенцию через конструктор.
          </div>

          <div v-else-if="viewMode === 'table'" class="table-responsive">
            <table class="table table-hover align-middle">
              <thead>
                <tr>
                  <th>Название</th>
                  <th class="d-none d-md-table-cell">Уровень</th>
                  <th class="d-none d-md-table-cell">Тип</th>
                  <th class="text-end">Популярность</th>
                  <th class="text-end d-none d-md-table-cell">Релевантность</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="comp in displayedItems"
                  :key="comp.id"
                  :class="comp.is_core ? 'cc-competence-row-core' : ''"
                >
                  <td>
                    <div class="fw-semibold">{{ comp.name }}</div>
                    <div v-if="comp.description" class="text-muted small">
                      {{ comp.description }}
                    </div>
                    <div v-if="comp.tags?.length" class="mt-1 d-flex flex-wrap gap-1">
                      <span
                        v-for="tag in comp.tags"
                        :key="tag"
                      class="badge cc-competence-tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </td>
                  <td class="d-none d-md-table-cell">
                    <span v-if="comp.level_display" class="badge cc-badge-level">
                      {{ comp.level_display }}
                    </span>
                  </td>
                  <td class="d-none d-md-table-cell">
                    <span
                      class="badge d-inline-flex align-items-center gap-1 cc-badge-type"
                      :class="comp.is_core ? 'cc-badge-type-base' : 'cc-badge-type-narrow'"
                    >
                      <component :is="comp.is_core ? Shield : Flame" :size="12" />
                      {{ comp.is_core ? 'Базовая' : 'Узконаправленная' }}
                    </span>
                  </td>
                  <td class="text-end">
                    {{ comp.popularity }}
                  </td>
                  <td class="text-end d-none d-md-table-cell">
                    {{ (comp.relevance ?? 0).toFixed(2) }}
                  </td>
                  <td class="text-end">
                    <button
                      class="btn btn-sm btn-outline-primary"
                      type="button"
                      @click="openDetail(comp.id)"
                    >
                      Открыть
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="row g-3">
            <div
              v-for="comp in displayedItems"
              :key="comp.id"
              class="col-12 col-md-6 col-lg-4"
            >
              <div class="card h-100 shadow-sm border-0 cc-competence-card">
                <div class="card-body d-flex flex-column">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                      <h5 class="mb-1">{{ comp.name }}</h5>
                      <div class="text-muted small" v-if="comp.level_display">
                        Уровень:
                        <span class="badge cc-badge-level ms-1">{{ comp.level_display }}</span>
                      </div>
                    </div>
                    <span
                      class="badge d-inline-flex align-items-center gap-1 cc-badge-type"
                      :class="comp.is_core ? 'cc-badge-type-base' : 'cc-badge-type-narrow'"
                    >
                      <component :is="comp.is_core ? Shield : Flame" :size="12" />
                      {{ comp.is_core ? 'Базовая' : 'Узконаправленная' }}
                    </span>
                  </div>

                  <p class="text-muted small mb-2" v-if="comp.description">
                    {{ comp.description }}
                  </p>

                  <div v-if="comp.tags?.length" class="d-flex flex-wrap gap-1 mb-2">
                    <span
                      v-for="tag in comp.tags"
                      :key="tag"
                      class="badge cc-competence-tag"
                    >
                      {{ tag }}
                    </span>
                  </div>

                  <div class="mt-auto d-flex justify-content-between align-items-center">
                    <div class="text-muted small">
                      Популярность: <strong>{{ comp.popularity }}</strong><br />
                      Релевантность: <strong>{{ (comp.relevance ?? 0).toFixed(2) }}</strong>
                    </div>
                    <button
                      class="btn btn-sm btn-outline-primary"
                      type="button"
                      @click="openDetail(comp.id)"
                    >
                      Открыть
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showDesigner"
      class="modal fade show d-block cc-competence-modal"
      tabindex="-1"
      role="dialog"
      aria-modal="true"
      @click.self="toggleDesigner"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Конструктор компетенции</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="toggleDesigner"></button>
          </div>
          <div class="modal-body">
            <p class="text-muted small mb-3">
              Заполните обязательные атрибуты, чтобы сформировать карточку компетенции для витрины.
            </p>

            <div class="cc-designer-hint mb-3">
              <Info :size="40" class="text-danger" />
              <span>
                Обязательные поля — наименование и уровень; тип: базовая (T‑shaped core) или узконаправленная; метрики: популярность 0–100%, релевантность 0–1.
              </span>
            </div>

            <div class="mb-3">
              <label class="form-label small text-muted">Название компетенции</label>
              <input
                v-model="draft.name"
                type="text"
                class="form-control"
                placeholder="Например, Backend разработка (Python/FastAPI)"
              />
            </div>

            <div class="mb-3">
              <label class="form-label small text-muted">Краткое описание</label>
              <textarea
                v-model="draft.description"
                class="form-control"
                rows="3"
                placeholder="Опишите, какие задачи и зона ответственности покрываются компетенцией"
              />
            </div>

            <div class="row g-2 mb-3 align-items-stretch">
              <div class="col-6">
                <div class="cc-field-box h-100">
                  <label class="form-label small text-muted">Уровень</label>
                  <select v-model="draft.level" class="form-select">
                    <option value="JUNIOR">Начинающий</option>
                    <option value="MIDDLE">Средний</option>
                    <option value="SENIOR">Опытный</option>
                    <option value="EXPERT">Экспертный</option>
                  </select>
                  <div class="text-muted small">Уровень соответствует ожидаемой зрелости специалиста и глубине компетенции.</div>
                </div>
              </div>
              <div class="col-6">
                <div class="cc-field-box h-100 d-flex flex-column">
                  <label class="form-label small text-muted d-block mb-1">Тип компетенции</label>
                  <div class="cc-core-toggle" role="group" aria-label="Тип компетенции">
                    <button
                      type="button"
                      class="cc-core-toggle-btn"
                      :class="{ active: draft.is_core }"
                      @click="draft.is_core = true"
                    >
                      <Shield :size="16" /> Базовая
                    </button>
                    <button
                      type="button"
                      class="cc-core-toggle-btn"
                      :class="{ active: !draft.is_core }"
                      @click="draft.is_core = false"
                    >
                      <Flame :size="16" /> Узконаправленная
                    </button>
                  </div>
                  <div class="text-muted small mt-1">Выберите профиль: базовая для широкой опоры, узконаправленная для глубокой специализации.</div>
                </div>
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label small text-muted">Теги (через запятую)</label>
              <input
                v-model="draft.tagsInput"
                type="text"
                class="form-control"
                placeholder="API, PostgreSQL, Celery"
              />
            </div>

            <div class="row g-2">
              <div class="col-6">
                <label class="form-label small text-muted">Популярность, %</label>
                <input
                  v-model.number="draft.popularity"
                  type="number"
                  min="0"
                  max="100"
                  class="form-control"
                />
              </div>
              <div class="col-6">
                <label class="form-label small text-muted">Релевантность (0–1)</label>
                <input
                  v-model.number="draft.relevance"
                  type="number"
                  min="0"
                  max="1"
                  step="0.01"
                  class="form-control"
                />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary btn-sm" @click="resetDraft">
              Очистить
            </button>
            <button
              type="button"
              class="btn btn-danger btn-sm"
              :disabled="!canSaveDraft"
              @click="saveDraft"
            >
              Сформировать черновик
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { BadgeCheck } from 'lucide-vue-next'
import { Filter, LayoutDashboard, Layers, Shield, Flame, Sparkle, Gauge, Search, Info } from 'lucide-vue-next'
import { useCompetencesListPage } from '../js/useCompetencesListPage.js'

const {
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
} = useCompetencesListPage()
</script>

<style scoped src="../scss/CompetencesListPage.scss"></style>


