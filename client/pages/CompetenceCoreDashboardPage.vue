<template>
  <div class="container py-4">
    <div class="cc-dashboard-header">
      <h2 class="mb-1 cc-dashboard-title d-flex align-items-center gap-2">
        <LayoutDashboard :size="26" :stroke-width="1.7" class="cc-dashboard-title-icon" />
        <span>Панель управления модулем компетенций</span>
      </h2>
      <p class="mb-0 cc-dashboard-subtitle">
        Здесь собраны основные разделы модуля: технологии, компетенции и профили вакансий.
        Выберите нужный блок, чтобы перейти к управлению данными.
      </p>
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
  </div>
</template>

<script setup>
import { useCompetenceCoreDashboardPage } from '../js/useCompetenceCoreDashboardPage.js'

const { LayoutDashboard, sections, goTo } = useCompetenceCoreDashboardPage()
</script>

<style scoped src="../scss/CompetenceCoreDashboardPage.scss"></style>


