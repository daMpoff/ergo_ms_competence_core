<template>
  <div class="container py-4">
    <div class="cc-vacancies-header d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-2 mb-3">
      <div class="d-flex align-items-center gap-2">
        <div class="cc-vacancies-title-icon d-flex align-items-center justify-content-center">
          <BriefcaseBusiness :size="22" :stroke-width="1.7" />
        </div>
        <div>
          <h2 class="mb-1 d-flex align-items-center gap-2">
            Профили вакансий
            <span class="badge cc-badge-accent">{{ stats.total }} профилей</span>
          </h2>
          <div class="text-muted small d-flex flex-wrap align-items-center gap-2">
            <span>Отслеживайте вакансии и требуемые компетенции по источникам, стеку и минимальному количеству навыков.</span>
            <span class="badge cc-badge-track" v-if="stats.tracked">
              В отслеживании: {{ stats.tracked }}
            </span>
          </div>
        </div>
      </div>
      <div class="d-flex flex-wrap gap-2 justify-content-start justify-content-lg-end">
        <button class="btn btn-outline-secondary btn-sm" type="button" @click="reload">
          Обновить данные
        </button>
        <div class="btn-group" role="group">
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

    <div class="card shadow-sm border-0 mb-3 cc-vacancies-filters-card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start mb-2 cc-vacancies-filters-header">
          <div class="d-flex align-items-center gap-2">
            <Filter :size="16" />
            <span class="fw-semibold">Фильтры и отслеживание</span>
          </div>
          <button class="btn btn-link btn-sm text-decoration-none p-0" type="button" @click="resetFilters">
            Сбросить
          </button>
        </div>
        <div class="row g-2 align-items-end cc-filters-row">
          <div class="col-12 col-md-5 col-lg-4">
            <label class="form-label small text-muted">Поиск по вакансии или тегам</label>
            <div class="input-group">
              <span class="input-group-text"><Search :size="16" /></span>
              <input
                v-model="search"
                type="text"
                class="form-control"
                placeholder="Название, стек или теги"
                @keyup.enter="reload"
              />
            </div>
          </div>
          <div class="col-12 col-md-3 col-lg-2">
            <label class="form-label small text-muted">Источник</label>
            <input
              v-model="source"
              type="text"
              class="form-control"
              placeholder="HeadHunter, Habr..."
              @keyup.enter="reload"
            />
          </div>
          <div class="col-12 col-md-4 col-lg-3">
            <label class="form-label small text-muted">Искомая компетенция / навык</label>
            <input
              v-model="competenceQuery"
              type="text"
              class="form-control"
              placeholder="Например, Python, DevOps..."
              @keyup.enter="reload"
            />
          </div>
          <div class="col-6 col-md-3 col-lg-2">
            <label class="form-label small text-muted">Мин. компетенций</label>
            <input
              v-model.number="minCompetences"
              type="number"
              min="0"
              class="form-control"
              placeholder="0"
              @keyup.enter="reload"
            />
          </div>
          <div class="col-6 col-md-3 col-lg-2">
            <label class="form-label small text-muted">Сортировка</label>
            <select v-model="sortBy" class="form-select">
              <option value="created_desc">Сначала новые</option>
              <option value="created_asc">Сначала старые</option>
              <option value="competences_desc">Больше компетенций</option>
              <option value="competences_asc">Меньше компетенций</option>
              <option value="title_asc">Название A–Я</option>
              <option value="title_desc">Название Я–А</option>
            </select>
          </div>
          <div class="col-12 col-md-3 col-lg-2 d-flex">
            <button
              type="button"
              class="btn btn-outline-secondary w-100"
              @click="reload"
            >
              Применить
            </button>
          </div>
        </div>
        <div v-if="topSources.length" class="cc-quick-pills mt-2">
          <span class="text-muted small me-2">Быстрый фильтр по источнику:</span>
          <button
            v-for="src in topSources"
            :key="src.name"
            type="button"
            class="btn btn-light btn-sm cc-quick-pill"
            @click="setSourceFilter(src.name)"
          >
            {{ src.name }} ({{ src.count }})
          </button>
        </div>
        <div v-if="activeFilters.length" class="cc-active-filters mt-3">
          <span class="text-muted small me-2">Активные фильтры:</span>
          <button
            v-for="flt in activeFilters"
            :key="`${flt.key}-${flt.value}`"
            type="button"
            class="btn btn-sm cc-filter-chip"
            @click="clearFilter(flt.key)"
          >
            <span class="fw-semibold">{{ flt.label }}:</span>
            <span>{{ flt.value }}</span>
            <X :size="14" />
          </button>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-3">
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body cc-kpi-body">
            <div class="cc-kpi-head">
              <div class="d-flex align-items-center gap-2">
                <span class="cc-kpi-dot"></span>
                <span class="cc-kpi-label">Всего профилей</span>
              </div>
              <span class="cc-vacancies-kpi-icon"><Layers :size="28" /></span>
            </div>
            <div class="cc-kpi-value-main">{{ stats.total }}</div>
            <div class="cc-kpi-pill">
              В отслеживании: <strong>{{ stats.tracked }}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body cc-kpi-body">
            <div class="cc-kpi-head">
              <div class="d-flex align-items-center gap-2">
                <span class="cc-kpi-dot"></span>
                <span class="cc-kpi-label">Источников</span>
              </div>
              <span class="cc-vacancies-kpi-icon"><Radar :size="28" /></span>
            </div>
            <div class="cc-kpi-value-main">{{ stats.sources }}</div>
            <div class="cc-kpi-pill">
              Топ: <strong>{{ topSources[0]?.name || '—' }}</strong>
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body cc-kpi-body">
            <div class="cc-kpi-head">
              <div class="d-flex align-items-center gap-2">
                <span class="cc-kpi-dot"></span>
                <span class="cc-kpi-label">Среднее число компетенций</span>
              </div>
              <span class="cc-vacancies-kpi-icon"><ListChecks :size="28" /></span>
            </div>
            <div class="cc-kpi-value-main">{{ stats.avgCompetences }}</div>
            <div class="cc-kpi-pill">
              Фильтр: ≥ {{ minCompetences || 0 }}
            </div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body cc-kpi-body">
            <div class="cc-kpi-head">
              <div class="d-flex align-items-center gap-2">
                <span class="cc-kpi-dot"></span>
                <span class="cc-kpi-label">Последнее обновление</span>
              </div>
              <span class="cc-vacancies-kpi-icon"><CalendarClock :size="28" /></span>
            </div>
            <div class="cc-kpi-value-main cc-vacancies-kpi-date">
              {{ stats.lastUpdatedFormatted }}
            </div>
            <div class="cc-kpi-pill">По поступившим данным</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5 cc-vacancies-loading">
      Загрузка витрины профилей...
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div v-if="displayedItems.length === 0" class="alert alert-info">
        Профили вакансий не найдены. Попробуйте изменить фильтры.
      </div>

      <div v-else-if="viewMode === 'table'" class="table-responsive">
        <table class="table table-hover align-middle cc-vacancies-table">
          <thead>
            <tr>
              <th>Вакансия</th>
              <th class="d-none d-md-table-cell">Источник</th>
              <th class="text-center d-none d-md-table-cell">Компетенций</th>
              <th class="text-center d-none d-md-table-cell">Отслеживание</th>
              <th class="text-end">Создан</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="profile in displayedItems"
              :key="profile.id"
              :class="{ 'is-tracked': isTracked(profile.id) }"
            >
              <td>
                <div class="fw-semibold">
                  {{ profile.vacancy_title }}
                </div>
                <div class="text-muted small" v-if="profile.location">
                  {{ profile.location }}
                </div>
                <div class="d-flex flex-wrap gap-1 mt-1" v-if="profile.tags?.length">
                  <span v-for="tag in profile.tags" :key="tag" class="badge cc-vacancy-tag">
                    {{ tag }}
                  </span>
                </div>
              </td>
              <td class="d-none d-md-table-cell">
                <span class="badge cc-badge-source">
                  {{ profile.vacancy_source || '—' }}
                </span>
              </td>
              <td class="text-center d-none d-md-table-cell">
                <span class="badge cc-badge-competence">
                  {{ profile.competences_count ?? '—' }}
                </span>
              </td>
              <td class="text-end">
                <div class="d-flex flex-column align-items-end gap-1">
                  <div class="text-muted small">
                    {{ formatDate(profile.created_at) }}
                  </div>
                  <span v-if="isFresh(profile)" class="badge cc-badge-fresh">Новый</span>
                  <div class="text-muted small" v-if="profile.salary">
                    {{ profile.salary }}
                  </div>
                </div>
              </td>
              <td class="text-end">
                <div class="d-flex justify-content-end align-items-center gap-2">
                  <button
                    type="button"
                    class="btn btn-sm cc-btn-track"
                    :class="isTracked(profile.id) ? 'btn-danger' : 'btn-outline-secondary'"
                    @click="onToggleTrack(profile.id)"
                  >
                    <component :is="isTracked(profile.id) ? BookmarkCheck : BookmarkPlus" :size="14" />
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    type="button"
                    @click="openDetail(profile.id)"
                  >
                    Открыть
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="row g-3">
        <div
          v-for="profile in displayedItems"
          :key="profile.id"
          class="col-12 col-md-6 col-lg-4"
        >
          <div class="card h-100 shadow-sm border-0 cc-vacancies-card">
            <div class="card-body d-flex flex-column">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                  <h5 class="mb-1">{{ profile.vacancy_title }}</h5>
                  <div class="text-muted small" v-if="profile.location">
                    {{ profile.location }}
                  </div>
                </div>
                <span class="badge cc-badge-source">
                  {{ profile.vacancy_source || '—' }}
                </span>
              </div>

              <div class="text-muted small mb-2 cc-vacancy-meta">
                <span class="badge cc-badge-competence">
                  {{ profile.competences_count ?? '—' }} компетенций
                </span>
                <span v-if="profile.salary" class="badge cc-badge-salary">
                  {{ profile.salary }}
                </span>
                <span v-if="isFresh(profile)" class="badge cc-badge-fresh">Новый</span>
              </div>

              <div v-if="profile.tags?.length" class="d-flex flex-wrap gap-1 mb-3">
                <span
                  v-for="tag in profile.tags"
                  :key="tag"
                  class="badge cc-vacancy-tag"
                >
                  {{ tag }}
                </span>
              </div>

              <div class="mt-auto d-flex justify-content-between align-items-center gap-2">
                <div class="text-muted small">
                  {{ formatDate(profile.created_at) }}
                </div>
                <div class="d-flex align-items-center gap-2">
                  <button
                    type="button"
                    class="btn btn-sm cc-btn-track"
                    :class="isTracked(profile.id) ? 'btn-danger' : 'btn-outline-secondary'"
                    @click="onToggleTrack(profile.id)"
                    :title="isTracked(profile.id) ? 'Убрать из отслеживания' : 'Отслеживать профиль'"
                  >
                    <component :is="isTracked(profile.id) ? BookmarkCheck : BookmarkPlus" :size="14" />
                  </button>
                  <button
                    class="btn btn-sm btn-outline-primary"
                    type="button"
                    @click="openDetail(profile.id)"
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
</template>

<script setup>
import { useToast } from 'vue-toastification'
import {
  BookmarkCheck,
  BookmarkPlus,
  BriefcaseBusiness,
  CalendarClock,
  Filter,
  Layers,
  ListChecks,
  Radar,
  Search,
  X,
} from 'lucide-vue-next'
import { useVacancyProfilesListPage } from '../js/useVacancyProfilesListPage.js'

const toast = useToast()

const {
  search,
  source,
  viewMode,
  competenceQuery,
  minCompetences,
  sortBy,
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
} = useVacancyProfilesListPage()

const onToggleTrack = (id) => {
  const tracked = toggleTrack(id)
  if (tracked) {
    toast.success('Профиль добавлен в отслеживание')
  } else {
    toast.info('Профиль убран из отслеживания')
  }
}
</script>

<style scoped src="../scss/VacancyProfilesListPage.scss"></style>

