<template>
  <div class="container py-4" v-if="!loading && profile">
    <div class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-start mb-3">
      <div>
        <h2 class="mb-1">{{ profile.vacancy_title }}</h2>
        <div class="text-muted d-flex flex-wrap gap-2 small">
          <span v-if="profile.vacancy_source" class="badge bg-light text-dark">
            {{ profile.vacancy_source }}
          </span>
          <span v-if="profile.location" class="badge bg-light text-dark">
            {{ profile.location }}
          </span>
          <span v-if="profile.salary" class="badge bg-light text-dark">
            {{ profile.salary }}
          </span>
        </div>
      </div>
      <div v-if="profile.tags?.length" class="mt-2 mt-lg-0 d-flex flex-wrap gap-1">
        <span v-for="tag in profile.tags" :key="tag" class="badge bg-light text-dark">
          {{ tag }}
        </span>
      </div>
    </div>

    <div class="card mb-4 shadow-sm border-0">
      <div class="card-body">
        <h5 class="card-title mb-3">Информация о вакансии</h5>
        <div v-if="profile.vacancy_info">
          <div class="mb-1">
            <strong>Название:</strong>
            <span>{{ profile.vacancy_info.title }}</span>
          </div>
          <div v-if="profile.vacancy_info.company" class="mb-1">
            <strong>Компания:</strong>
            <span>{{ profile.vacancy_info.company }}</span>
          </div>
          <div v-if="profile.vacancy_info.city" class="mb-1">
            <strong>Город:</strong>
            <span>{{ profile.vacancy_info.city }}</span>
          </div>
          <div v-if="profile.vacancy_info.url" class="mb-1">
            <strong>Ссылка:</strong>
            <a :href="profile.vacancy_info.url" target="_blank" rel="noopener">
              Открыть вакансию
            </a>
          </div>
        </div>
        <div v-else class="text-muted">
          Детальная информация о вакансии недоступна.
        </div>
      </div>
    </div>

    <h5 class="mb-3 d-flex align-items-center gap-2">
      Компетенции профиля
      <span class="badge bg-secondary">{{ competences.length }}</span>
    </h5>

    <div v-if="competences.length === 0" class="alert alert-info">
      Для этой вакансии ещё не заданы компетенции.
    </div>

    <div v-else class="table-responsive">
      <table class="table table-sm table-hover align-middle">
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
              {{ item.priority }}
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span v-if="item.required_level_display" class="badge bg-light text-dark">
                {{ item.required_level_display }}
              </span>
            </td>
            <td class="text-center d-none d-md-table-cell">
              <span
                class="badge"
                :class="item.is_mandatory ? 'bg-success' : 'bg-outline-secondary'"
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
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useVacancyProfileDetail } from '../js/useVacancyProfiles.js'

const route = useRoute()
const { profile, competences, loading, error, fetchProfile } = useVacancyProfileDetail()

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    fetchProfile(id)
  }
})
</script>


