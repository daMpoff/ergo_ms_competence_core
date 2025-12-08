<template>
  <div class="container py-4">
    <div class="cc-vacancies-header d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-2 mb-3">
      <div class="d-flex align-items-center gap-2">
        <div class="cc-vacancies-title-icon d-flex align-items-center justify-content-center">
          <BriefcaseBusiness :size="22" :stroke-width="1.7" />
        </div>
        <div>
          <h2 class="mb-1">Профили вакансий</h2>
          <p class="text-muted mb-0">
            Анализируйте витрину вакансий и их компетентностные матрицы по источникам и стеку.
          </p>
        </div>
      </div>
      <div class="d-flex flex-wrap gap-2 justify-content-start justify-content-lg-end">
        <button class="btn btn-outline-secondary" type="button" @click="reload">
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

    <div class="card shadow-sm border-0 mb-3">
      <div class="card-body">
        <div class="row g-2 align-items-end">
          <div class="col-12 col-md-6 col-lg-4">
            <label class="form-label small text-muted">Поиск по вакансии</label>
            <input
              v-model="search"
              type="text"
              class="form-control"
              placeholder="Название, стек или теги"
              @keyup.enter="reload"
            />
          </div>
          <div class="col-12 col-md-4 col-lg-3">
            <label class="form-label small text-muted">Источник</label>
            <input
              v-model="source"
              type="text"
              class="form-control"
              placeholder="HeadHunter, Habr, ..."
              @keyup.enter="reload"
            />
          </div>
          <div class="col-12 col-md-2 col-lg-2 d-flex">
            <button
              type="button"
              class="btn btn-outline-secondary w-100"
              @click="reload"
            >
              Применить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-3">
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body">
            <div class="text-muted small">Всего профилей</div>
            <div class="h4 mb-0">{{ stats.total }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body">
            <div class="text-muted small">Источников</div>
            <div class="h4 mb-0">{{ stats.sources }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body">
            <div class="text-muted small">Среднее число компетенций</div>
            <div class="h4 mb-0">{{ stats.avgCompetences }}</div>
          </div>
        </div>
      </div>
      <div class="col-6 col-lg-3">
        <div class="card shadow-sm border-0 h-100 cc-vacancies-kpi-card">
          <div class="card-body">
            <div class="text-muted small">Последнее обновление</div>
            <div class="h6 mb-0">{{ stats.lastUpdatedFormatted }}</div>
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
      <div v-if="items.length === 0" class="alert alert-info">
        Профили вакансий не найдены. Попробуйте изменить фильтры.
      </div>

      <div v-else-if="viewMode === 'table'" class="table-responsive">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Вакансия</th>
              <th class="d-none d-md-table-cell">Источник</th>
              <th class="text-center d-none d-md-table-cell">Компетенций</th>
              <th class="text-end">Создан</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="profile in items" :key="profile.id">
              <td>
                <div class="fw-semibold">
                  {{ profile.vacancy_title }}
                </div>
                <div class="text-muted small" v-if="profile.location">
                  {{ profile.location }}
                </div>
                <div class="d-flex flex-wrap gap-1 mt-1" v-if="profile.tags?.length">
                  <span v-for="tag in profile.tags" :key="tag" class="badge bg-light text-dark">
                    {{ tag }}
                  </span>
                </div>
              </td>
              <td class="d-none d-md-table-cell">
                <span class="badge bg-light text-dark">
                  {{ profile.vacancy_source || '—' }}
                </span>
              </td>
              <td class="text-center d-none d-md-table-cell">
                {{ profile.competences_count ?? '—' }}
              </td>
              <td class="text-end">
                <div class="text-muted small">
                  {{ formatDate(profile.created_at) }}
                </div>
                <div class="text-muted small" v-if="profile.salary">
                  {{ profile.salary }}
                </div>
              </td>
              <td class="text-end">
                <button
                  class="btn btn-sm btn-outline-primary"
                  type="button"
                  @click="openDetail(profile.id)"
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
          v-for="profile in items"
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
                <span class="badge bg-light text-dark">
                  {{ profile.vacancy_source || '—' }}
                </span>
              </div>

              <div class="text-muted small mb-2">
                Компетенций: <strong>{{ profile.competences_count ?? '—' }}</strong><br />
                <span v-if="profile.salary">Зарплата: <strong>{{ profile.salary }}</strong></span>
              </div>

              <div v-if="profile.tags?.length" class="d-flex flex-wrap gap-1 mb-3">
                <span
                  v-for="tag in profile.tags"
                  :key="tag"
                  class="badge bg-light text-dark"
                >
                  {{ tag }}
                </span>
              </div>

              <div class="mt-auto d-flex justify-content-between align-items-center">
                <div class="text-muted small">
                  {{ formatDate(profile.created_at) }}
                </div>
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
</template>

<script setup>
import { BriefcaseBusiness } from 'lucide-vue-next'
import { useVacancyProfilesListPage } from '../js/useVacancyProfilesListPage.js'

const {
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
} = useVacancyProfilesListPage()
</script>

<style scoped src="../scss/VacancyProfilesListPage.scss"></style>

