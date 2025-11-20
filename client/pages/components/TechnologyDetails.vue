<template>
  <div>
    <div class="d-flex justify-content-between align-items-start" :class="{ 'mb-2': !isInTable }">
      <div class="tech-section-header">
        <span class="tech-section-title">Синонимы</span>
        <span v-if="technology.aliases_count" class="tech-section-count">
          ({{ technology.aliases_count }})
        </span>
        <span v-if="aliasesLoading" class="tech-section-status text-muted">
          Загрузка...
        </span>
        <span v-else-if="aliasesError" class="tech-section-status text-danger">
          {{ aliasesError }}
        </span>
      </div>
      <button
        v-if="isInTable"
        type="button"
        class="tech-close-btn"
        @click.stop="$emit('close')"
      >
        <span class="tech-close-btn-icon"></span>
      </button>
    </div>

    <div class="row g-2 align-items-start">
      <div class="col-12">
        <div v-if="aliases?.length" class="d-flex flex-wrap gap-2">
          <span v-for="alias in aliases" :key="alias.id" class="tech-alias-badge">
            {{ alias.alias }}
          </span>
        </div>
        <div v-else-if="!aliasesLoading" class="text-muted small">
          Синонимов не найдено.
        </div>
      </div>

      <div class="col-12">
        <div class="tech-section-header">
          <span class="tech-section-title">Дочерние технологии</span>
          <span v-if="technology.child_technologies_count" class="tech-section-count">
            ({{ technology.child_technologies_count }})
          </span>
        </div>
        <div v-if="childrenLoading" class="text-muted small">
          Загрузка...
        </div>
        <div v-else-if="childrenError" class="text-danger small">
          {{ childrenError }}
        </div>
        <div v-else-if="children?.length" class="d-flex flex-wrap gap-2">
          <span v-for="child in children" :key="child.id" class="tech-child-badge">
            {{ child.name }}
          </span>
        </div>
        <div v-else class="tech-section-empty">
          <span class="tech-section-empty-icon">
            <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true">
              <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.5" />
              <line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            </svg>
          </span>
          <span class="tech-section-empty-text">
            Дочерние технологии отсутствуют
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  technology: { type: Object, required: true },
  aliases: { type: Array, default: () => [] },
  aliasesLoading: { type: Boolean, default: false },
  aliasesError: { type: String, default: null },
  children: { type: Array, default: () => [] },
  childrenLoading: { type: Boolean, default: false },
  childrenError: { type: String, default: null },
  isInTable: { type: Boolean, default: false },
})

defineEmits(['close'])
</script>

