<template>
  <div class="container py-4" v-if="!loading && profile">
    <div class="cc-vp-header d-flex flex-column flex-lg-row justify-content-between align-items-lg-start gap-2 mb-3">
      <div class="d-flex align-items-start gap-3">
        <div class="cc-vp-icon">
          <BriefcaseBusiness :size="22" />
        </div>
        <div>
          <h2 class="mb-1">{{ profile.vacancy_title }}</h2>
          <div class="cc-vp-meta d-flex flex-wrap gap-2">
            <span v-if="profile.vacancy_source" class="badge cc-vp-chip">
              {{ profile.vacancy_source }}
            </span>
            <span v-if="profile.location" class="badge cc-vp-chip">
              {{ profile.location }}
            </span>
            <span v-if="profile.salary" class="badge cc-vp-chip cc-vp-chip--accent">
              {{ profile.salary }}
            </span>
          </div>
          <div v-if="profile.vacancy_info?.company" class="text-muted small mt-1">
            Компания: <strong>{{ profile.vacancy_info.company }}</strong>
          </div>
        </div>
      </div>
      <div v-if="profile.tags?.length" class="mt-1 mt-lg-0 d-flex flex-wrap gap-1">
        <span v-for="tag in profile.tags" :key="tag" class="badge cc-vacancy-tag">
          {{ tag }}
        </span>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-vp-card">
          <div class="card-body">
            <h6 class="text-muted text-uppercase small mb-2">Показатели</h6>
            <div class="cc-vp-kpi-grid">
              <div class="cc-vp-kpi">
                <div class="cc-vp-kpi-label">Популярность</div>
                <div class="cc-vp-kpi-value">{{ metrics.popularity }}%</div>
                <div class="cc-vp-kpi-bar">
                  <div :style="{ width: `${metrics.popularity}%` }"></div>
                </div>
              </div>
              <div class="cc-vp-kpi">
                <div class="cc-vp-kpi-label">Конкурентность</div>
                <div class="cc-vp-kpi-value">{{ metrics.competitiveness }}%</div>
                <div class="cc-vp-kpi-bar cc-vp-kpi-bar--accent">
                  <div :style="{ width: `${metrics.competitiveness}%` }"></div>
                </div>
              </div>
              <div class="cc-vp-kpi">
                <div class="cc-vp-kpi-label">Сложность</div>
                <div class="cc-vp-kpi-value">{{ metrics.complexity }}/10</div>
                <div class="cc-vp-kpi-bar cc-vp-kpi-bar--muted">
                  <div :style="{ width: `${(metrics.complexity / 10) * 100}%` }"></div>
                </div>
              </div>
            </div>
            <div class="text-muted small mt-2">
              Оценки рассчитываются по числу компетенций, весам и приоритетам профиля.
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0 h-100 cc-vp-card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="card-title mb-0">Матрица уровней компетенций</h5>
              <span class="badge cc-vp-count">{{ competences.length }}</span>
            </div>
            <p class="text-muted small mb-3">
              Распределение компетенций по требуемым уровням и обязательности.
            </p>
            <div v-if="matrixRows.length === 0" class="text-muted small">
              Недостаточно данных для построения матрицы.
            </div>
            <div v-else class="table-responsive">
              <table class="table table-sm align-middle cc-vp-table">
                <thead>
                  <tr>
                    <th>Уровень</th>
                    <th
                      v-for="col in levelColumns"
                      :key="col"
                      class="text-center"
                    >
                      {{ col }}
                    </th>
                    <th class="text-center">Всего</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in matrixRows" :key="row.category">
                    <td>
                      <div class="fw-semibold">{{ row.category }}</div>
                    </td>
                    <td
                      v-for="col in levelColumns"
                      :key="col"
                      class="text-center"
                    >
                      <div class="cc-vp-matrix-cell">
                        <span class="cc-vp-matrix-count">
                          {{ row.levels[col] }}
                        </span>
                        <div class="cc-vp-matrix-bar">
                          <div
                            :style="{
                              width: row.max > 0 ? `${(row.levels[col] / row.max) * 100}%` : '0%',
                            }"
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td class="text-center fw-semibold">{{ row.total }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-7">
        <div class="card shadow-sm border-0 h-100 cc-vp-card">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="card-title mb-0">Информация о вакансии</h5>
              <span v-if="profile.vacancy_info?.url" class="badge cc-vp-chip">
                <a :href="profile.vacancy_info.url" target="_blank" rel="noopener" class="cc-vp-link">Открыть</a>
              </span>
            </div>
            <div v-if="profile.vacancy_info" class="cc-vp-grid">
              <div>
                <div class="cc-vp-label">Название</div>
                <div class="cc-vp-value">{{ profile.vacancy_info.title }}</div>
              </div>
              <div v-if="profile.vacancy_info.company">
                <div class="cc-vp-label">Компания</div>
                <div class="cc-vp-value">{{ profile.vacancy_info.company }}</div>
              </div>
              <div v-if="profile.vacancy_info.city">
                <div class="cc-vp-label">Город</div>
                <div class="cc-vp-value">{{ profile.vacancy_info.city }}</div>
              </div>
            </div>
            <div v-else class="text-muted">
              Детальная информация о вакансии недоступна.
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-5">
        <div class="card shadow-sm border-0 h-100 cc-vp-card">
          <div class="card-body">
            <h5 class="card-title mb-3">Итого по профилю</h5>
            <div class="d-flex flex-wrap gap-2 cc-vp-stats">
              <span class="badge cc-vp-pill">
                Компетенций: <strong>{{ competences.length }}</strong>
              </span>
              <span class="badge cc-vp-pill">
                Источник: <strong>{{ profile.vacancy_source || '—' }}</strong>
              </span>
              <span class="badge cc-vp-pill">
                Зарплата: <strong>{{ profile.salary || '—' }}</strong>
              </span>
            </div>
            <div class="text-muted small mt-2">
              Матрица компетенций помогает оценить требования к кандидату.
            </div>
          </div>
        </div>
      </div>
    </div>

    <h5 class="mb-3 d-flex align-items-center gap-2 cc-vp-title">
      Компетенции профиля
      <span class="badge cc-vp-count">{{ competences.length }}</span>
    </h5>

    <div v-if="competences.length === 0" class="alert alert-info">
      Для этой вакансии ещё не заданы компетенции.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-sm table-hover align-middle cc-vp-table">
        <thead>
          <tr>
            <th>Компетенция</th>
            <th class="text-center">Приоритет</th>
            <th class="text-center d-none d-md-table-cell">Уровень</th>
            <th class="text-center d-none d-md-table-cell">Обязательная</th>
            <th class="text-center d-none d-md-table-cell">Вес</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in competences" :key="item.id">
            <td>
              <div class="fw-semibold">
                {{ item.competence_name }}
              </div>
            </td>
            <td class="text-center">
              <span class="badge cc-vp-badge">{{ item.priority }}</span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span v-if="item.required_level_display" class="badge cc-vp-badge cc-vp-badge--soft">
                {{ item.required_level_display }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span
                class="badge"
                :class="item.is_mandatory ? 'cc-vp-badge cc-vp-badge--accent' : 'cc-vp-badge cc-vp-badge--muted'"
              >
                {{ item.is_mandatory ? 'Да' : 'Нет' }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              {{ (item.weight ?? 0).toFixed(2) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div v-else-if="loading" class="container py-5 text-center">
    Загрузка...
  </div>

  <div v-else-if="error" class="container py-5">
    <div class="alert alert-danger">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { BriefcaseBusiness } from 'lucide-vue-next'
import { useVacancyProfileDetail } from '../js/useVacancyProfiles.js'

const route = useRoute()
const { profile, competences, loading, error, fetchProfile } = useVacancyProfileDetail()

const metrics = computed(() => {
  const list = competences.value || []
  const count = list.length
  const avgWeight =
    count === 0 ? 0 : list.reduce((sum, c) => sum + (Number(c.weight) || 0), 0) / count
  const avgPriority =
    count === 0 ? 0 : list.reduce((sum, c) => sum + (Number(c.priority) || 0), 0) / count
  const popularity = Math.min(100, Math.round(count * 8 + avgWeight * 50))
  const competitiveness = Math.min(100, Math.round((avgWeight || 0) * 120 + avgPriority * 5))
  const complexity = Math.min(10, Math.max(1, Math.round((avgPriority || 0) / 2)))
  return { popularity, competitiveness, complexity }
})

const levelColumns = ['Junior', 'Middle', 'Senior', 'Lead']

const matrixRows = computed(() => {
  const list = competences.value || []
  if (!list.length) return []
  const map = new Map()
  const levels = levelColumns
  const categoryKey = (isMandatory) => (isMandatory ? 'Обязательные' : 'Опциональные')

  list.forEach((c) => {
    const category = categoryKey(!!c.is_mandatory)
    if (!map.has(category)) {
      const base = {}
      levels.forEach((lvl) => {
        base[lvl] = 0
      })
      map.set(category, { category, levels: base, total: 0, max: 0 })
    }
    const row = map.get(category)
    const lvl = levels.includes(c.required_level_display) ? c.required_level_display : 'Middle'
    row.levels[lvl] += 1
    row.total += 1
    row.max = Math.max(row.max, row.levels[lvl])
  })

  return Array.from(map.values())
})

onMounted(() => {
  const raw = route.params.id
  const numeric = Number(raw)
  const id = Number.isNaN(numeric) ? raw : numeric
  if (id) {
    fetchProfile(id)
  }
})
</script>

<style scoped src="../scss/VacancyProfileDetailPage.scss"></style>


