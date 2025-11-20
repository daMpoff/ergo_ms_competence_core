<template>
  <div class="table-responsive">
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
        <template v-for="tech in items" :key="tech.id">
          <tr
            class="tech-row"
            :class="{ 'table-active': expandedId === tech.id }"
            @click="$emit('toggleExpanded', tech)"
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
                <TechnologyDetails
                  :technology="tech"
                  :aliases="aliasesById[tech.id]"
                  :aliases-loading="aliasesLoading[tech.id]"
                  :aliases-error="aliasesError[tech.id]"
                  :children="childrenById[tech.id]"
                  :children-loading="childrenLoading[tech.id]"
                  :children-error="childrenError[tech.id]"
                  :is-in-table="true"
                  @close="$emit('toggleExpanded', tech, true)"
                />
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import TechnologyDetails from './TechnologyDetails.vue'

defineProps({
  items: { type: Array, required: true },
  expandedId: { type: [Number, String, null], default: null },
  aliasesById: { type: Object, required: true },
  aliasesLoading: { type: Object, required: true },
  aliasesError: { type: Object, required: true },
  childrenById: { type: Object, required: true },
  childrenLoading: { type: Object, required: true },
  childrenError: { type: Object, required: true },
  categoryIcon: { type: Function, required: true },
  categoryIconClass: { type: Function, required: true },
  popularityPercent: { type: Function, required: true },
})

defineEmits(['toggleExpanded'])
</script>

