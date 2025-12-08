<template>
  <div class="container py-4">
    <div class="cc-dashboard-header">
      <h2 class="mb-1 cc-dashboard-title d-flex align-items-center gap-2">
        <LayoutDashboard :size="26" :stroke-width="1.7" class="cc-dashboard-title-icon" />
          <span>Панель управления модулем компетенций</span>
      </h2>
      <p class="mb-0 cc-dashboard-subtitle">
          Аналитика по технологиям, компетенциям и профилям вакансий: ключевые KPI, динамика популярности
          и прогнозы для быстрых управленческих решений.
      </p>
    </div>

    <div class="card shadow-sm border-0 mb-3">
      <div class="card-body cc-filter-panel">
        <div class="cc-filter-header d-flex justify-content-between align-items-start">
          <div>
            <div class="cc-filter-title">Настройка витрины</div>
            <div class="cc-filter-note text-muted small">Обновляется мгновенно</div>
          </div>
          <div class="cc-filter-period">
            <span class="text-muted small me-2">Период</span>
            <div class="btn-group btn-group-sm" role="group" aria-label="Период">
              <button
                v-for="period in periods"
                :key="period.value"
                type="button"
                class="btn"
                :class="period.value === selectedPeriod ? 'btn-danger' : 'btn-outline-secondary'"
                @click="setPeriod(period.value)"
              >
                {{ period.label }}
              </button>
            </div>
          </div>
        </div>
        <div class="cc-filter-row">
          <div class="cc-filter-section">
            <div class="cc-filter-label text-muted small">Технологии</div>
            <div class="d-flex flex-wrap gap-2">
              <label
                v-for="tech in techPool"
                :key="tech"
                class="cc-chip"
              >
                <input
                  type="checkbox"
                  class="form-check-input me-1"
                  :checked="selectedTechnologies.includes(tech)"
                  @change="toggleTechnology(tech)"
                />
                <span>{{ tech }}</span>
              </label>
            </div>
          </div>
          <div class="cc-filter-section">
            <div class="cc-filter-label text-muted small">Категории</div>
            <div class="d-flex flex-wrap gap-2">
              <label
                v-for="cat in categoryPool"
                :key="cat"
                class="cc-chip cc-chip--muted"
              >
                <input
                  type="checkbox"
                  class="form-check-input me-1"
                  :checked="selectedCategories.includes(cat)"
                  @change="toggleCategory(cat)"
                />
                <span>{{ cat }}</span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div
        v-for="kpi in kpis"
        :key="kpi.id"
        class="col-6 col-lg-3"
      >
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="d-flex align-items-center gap-2 mb-2">
              <div class="kpi-icon">
                <component :is="kpi.icon" :size="18" />
              </div>
              <div class="text-muted small">{{ kpi.label }}</div>
            </div>
            <div class="h4 mb-0" :class="kpi.accent">{{ kpi.value }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="card-title mb-0">Динамика популярности технологий</h5>
              <span class="badge bg-light text-dark border">Период: {{ selectedPeriod }} мес</span>
            </div>
            <ApexCharts
              type="line"
              height="300"
              :options="popularityTrendOptions"
              :series="popularityTrendSeries"
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="card-title mb-2">Топ технологий (сейчас)</h5>
            <ApexCharts
              type="bar"
              height="300"
              :options="topTechnologiesOptions"
              :series="topTechnologiesSeries"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="card-title mb-2">Уровни компетенций</h5>
            <p class="text-muted small mb-2">Распределение по уровням</p>
            <ApexCharts
              type="donut"
              height="280"
              :options="levelOptions"
              :series="levelSeries"
            />
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-8">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="card-title mb-0">Категории технологий — динамика</h5>
            </div>
            <ApexCharts
              type="area"
              height="300"
              :options="categoryStackedOptions"
              :series="categoryStackedSeries"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-3 g-3 cc-dashboard-grid">
      <div
        v-for="section in sections"
        :key="section.id"
        class="col d-flex"
      >
        <div class="card h-100 shadow-sm border-0 cc-dashboard-card flex-fill">
          <div class="card-body d-flex flex-column">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <div class="d-flex align-items-center gap-2">
                <div
                  class="cc-dashboard-card-icon d-flex align-items-center justify-content-center"
                  :class="section.accentClass"
                >
                  <component
                    :is="section.icon"
                    :size="20"
                    :stroke-width="1.9"
                  />
                </div>
                <div>
                  <h5 class="card-title mb-0 cc-dashboard-card-title">
                    {{ section.title }}
                  </h5>
                  <div v-if="section.badge" class="small text-muted">
                    {{ section.badge }}
                  </div>
                </div>
              </div>
            </div>

            <p class="card-text text-muted small mb-3">
              {{ section.description }}
            </p>

            <div class="mt-auto">
              <button
                type="button"
                class="btn btn-sm btn-primary w-100 d-flex align-items-center justify-content-center gap-2"
                @click="goTo(section.routeName)"
              >
                <span>Перейти в раздел</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 cc-highlight-row">
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-highlight-card">
          <div class="card-body">
            <h6 class="card-title mb-2 d-flex align-items-center gap-2">
              <component :is="highlights.fastest.icon" :size="16" class="text-danger" />
              Быстрорастущая технология
            </h6>
            <div class="fw-semibold">{{ highlights.fastest.name }}</div>
            <div class="text-muted small mb-2">{{ highlights.fastest.delta }}</div>
            <p class="text-muted small mb-0">{{ highlights.fastest.note }}</p>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-highlight-card">
          <div class="card-body">
            <h6 class="card-title mb-2 d-flex align-items-center gap-2">
              <component :is="highlights.vacancy.icon" :size="16" class="text-danger" />
              Самая популярная вакансия
            </h6>
            <div class="fw-semibold">{{ highlights.vacancy.name }}</div>
            <div class="text-muted small mb-2">{{ highlights.vacancy.window }}</div>
            <p class="text-muted small mb-0">{{ highlights.vacancy.note }}</p>
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-4">
        <div class="card shadow-sm border-0 h-100 cc-highlight-card">
          <div class="card-body">
            <h6 class="card-title mb-2 d-flex align-items-center gap-2">
              <component :is="highlights.category.icon" :size="16" class="text-danger" />
              Лидер категории
            </h6>
            <div class="fw-semibold">{{ highlights.category.name }}</div>
            <div class="text-muted small mb-2">{{ highlights.category.share }}</div>
            <p class="text-muted small mb-0">{{ highlights.category.note }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0 mt-3">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-2">
          <h6 class="card-title mb-0">Рост / просадка за 30 дней</h6>
          <span class="text-muted small">Δ по популярности (п.п.)</span>
        </div>
        <div class="table-responsive">
          <table class="table table-sm align-middle mb-0">
            <thead>
              <tr class="text-muted small">
                <th scope="col">Технология</th>
                <th scope="col" class="text-end">Δ 30д</th>
                <th scope="col" class="text-center w-25">Мини-тренд</th>
                <th scope="col">Комментарий</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in growthSignals" :key="row.name">
                <td class="fw-semibold">
                  <span class="cc-growth-name">
                    <component
                      :is="row.icon"
                      :size="14"
                      :class="['cc-growth-name-icon', row.delta >= 0 ? 'text-danger' : 'text-muted']"
                    />
                    <span>{{ row.name }}</span>
                  </span>
                </td>
                <td class="text-end">
                  <span class="cc-pill" :class="row.delta >= 0 ? 'cc-pill-up' : 'cc-pill-down'">
                    {{ row.delta >= 0 ? '+' : '' }}{{ row.delta.toFixed(1) }} п.п.
                  </span>
                </td>
                <td class="text-center">
                  <div class="cc-spark" :title="row.trend.join(' → ')">
                    <span
                      v-for="(val, idx) in row.trend"
                      :key="idx"
                      class="cc-spark-dot"
                      :class="row.delta >= 0 ? 'cc-spark-dot-up' : 'cc-spark-dot-down'"
                      :style="{
                        opacity: Math.max(0.25, (val - row.trendMin) / (row.trendMax - row.trendMin + 0.01)),
                        height: `${6 + Math.max(0, (val - row.trendMin) / (row.trendMax - row.trendMin + 0.01) * 10)}px`
                      }"
                    />
                  </div>
                </td>
                <td class="text-muted small">{{ row.comment }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="row g-3 mt-3">
      <div class="col-12 col-lg-6">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6 class="card-title mb-0">Сравнение с прошлым периодом (топ‑5)</h6>
              <span class="text-muted small">Текущий vs прошлый период</span>
            </div>
            <ApexCharts
              type="bar"
              height="260"
              :options="comparisonOptions"
              :series="comparisonSeries"
            />
          </div>
        </div>
      </div>
      <div class="col-12 col-lg-6">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h6 class="card-title mb-0">Медианная ЗП по категориям технологий</h6>
              <span class="text-muted small">Текущие и 4 прогноза вперёд</span>
            </div>
            <ApexCharts
              type="line"
              height="260"
              :options="forecastOptions"
              :series="forecastSeries"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCompetenceCoreDashboardPage } from '../js/useCompetenceCoreDashboardPage.js'
import VueApexCharts from 'vue3-apexcharts'

const ApexCharts = VueApexCharts

const {
  LayoutDashboard,
  sections,
  kpis,
  periods,
  selectedPeriod,
  setPeriod,
  techPool,
  selectedTechnologies,
  toggleTechnology,
  categoryPool,
  selectedCategories,
  toggleCategory,
  popularityTrendSeries,
  popularityTrendOptions,
  categoryStackedSeries,
  categoryStackedOptions,
  topTechnologiesSeries,
  topTechnologiesOptions,
  levelSeries,
  levelOptions,
  growthSignals,
  highlights,
  comparisonSeries,
  comparisonOptions,
  forecastSeries,
  forecastOptions,
  goTo
} = useCompetenceCoreDashboardPage()
</script>

<style scoped src="../scss/CompetenceCoreDashboardPage.scss"></style>


