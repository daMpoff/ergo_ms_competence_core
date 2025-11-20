<template>
  <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">
    <div v-for="tech in items" :key="tech.id" class="col">
      <div
        class="card shadow-sm border-0 tech-card"
        :class="{ 'border-primary': expandedId === tech.id }"
      >
        <div class="card-body d-flex flex-column">
          <div class="tech-card-header d-flex justify-content-between align-items-start mb-2">
            <div class="me-2 flex-grow-1">
              <div class="d-flex align-items-center gap-2 mb-1">
                <div
                  v-if="tech.category"
                  class="tech-card-category-icon"
                  :class="categoryIconClass(tech.category)"
                >
                  <component
                    :is="categoryIcon(tech.category)"
                    :size="14"
                    stroke-width="1.8"
                  />
                </div>
                <h5 class="card-title mb-0 text-truncate" :title="tech.name">
                  {{ tech.name }}
                </h5>
              </div>
              <div v-if="tech.category_display" class="text-muted small mb-1">
                {{ tech.category_display }}
              </div>
              <div
                class="tech-card-meta text-muted small"
                v-if="tech.aliases_count || tech.child_technologies_count"
              >
                <span v-if="tech.aliases_count">
                  Синонимов: {{ tech.aliases_count }}
                </span>
                <span
                  v-if="tech.aliases_count && tech.child_technologies_count"
                  class="mx-1"
                >
                  •
                </span>
                <span v-if="tech.child_technologies_count">
                  Дочерние технологии: {{ tech.child_technologies_count }}
                </span>
              </div>
            </div>
            <div class="text-end small text-muted d-none d-lg-block ms-2">
              <div>Популярность: {{ popularityPercent(tech) }}%</div>
              <div>Упоминаний: {{ tech.occurrence_count ?? 0 }}</div>
            </div>
          </div>

          <p v-if="tech.description" class="card-text text-muted small mb-3">
            {{ tech.description }}
          </p>

          <div class="mt-auto">
            <div class="d-flex flex-wrap gap-2 mb-2 small">
              <span class="badge bg-light text-dark">
                Релевантность: {{ (tech.relevance ?? 0).toFixed(2) }}
              </span>
              <span class="badge bg-light text-dark">
                Упоминаний: {{ tech.occurrence_count ?? 0 }}
              </span>
            </div>

            <div class="mb-2">
              <div class="d-flex justify-content-between small">
                <span class="text-muted">Популярность</span>
                <span>{{ popularityPercent(tech) }}%</span>
              </div>
              <div class="progress" style="height: 4px">
                <div
                  class="progress-bar bg-primary"
                  role="progressbar"
                  :style="{ width: popularityPercent(tech) + '%' }"
                ></div>
              </div>
            </div>

            <button
              type="button"
              class="btn btn-sm btn-outline-primary w-100 d-flex align-items-center justify-content-center gap-1"
              @click.stop="$emit('toggleExpanded', tech)"
            >
              <span v-if="expandedId === tech.id">
                Скрыть
              </span>
              <span v-else>
                Подробнее
                <span v-if="tech.aliases_count">
                  ({{ tech.aliases_count }})
                </span>
              </span>
            </button>

            <Transition name="tech-expand">
              <div v-if="expandedId === tech.id" class="mt-2 border-top pt-2">
                <TechnologyDetails
                  :technology="tech"
                  :aliases="aliasesById[tech.id]"
                  :aliases-loading="aliasesLoading[tech.id]"
                  :aliases-error="aliasesError[tech.id]"
                  :children="childrenById[tech.id]"
                  :children-loading="childrenLoading[tech.id]"
                  :children-error="childrenError[tech.id]"
                  :is-in-table="false"
                />
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </div>
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

