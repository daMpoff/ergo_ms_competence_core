<template>
  <div class="mb-3">
    <div class="d-flex flex-wrap gap-2">
      <button
        type="button"
        class="btn btn-sm"
        :class="!category ? 'btn-primary' : 'btn-outline-primary'"
        @click="$emit('setCategory', '')"
      >
        Все категории
      </button>
      <button
        v-for="cat in categories"
        :key="cat.value"
        type="button"
        class="btn btn-sm"
        :class="category === cat.value ? 'btn-primary' : 'btn-outline-primary'"
        @click="$emit('setCategory', cat.value)"
      >
        {{ cat.label }}
      </button>
    </div>
    <Transition name="synonyms-hint">
      <div v-if="showSynonymsHint" class="tech-synonyms-hint mt-2">
        <span class="tech-synonyms-hint-icon">
          <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
            <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5" />
            <line x1="12" y1="10" x2="12" y2="16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            <circle cx="12" cy="7" r="1" fill="currentColor" />
          </svg>
        </span>
        <span class="tech-synonyms-hint-text">
          Нажмите по строке технологии или по кнопке в карточке для просмотра синонимов
        </span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
defineProps({
  category: { type: String, required: true },
  categories: { type: Array, required: true },
  showSynonymsHint: { type: Boolean, required: true },
})

defineEmits(['setCategory'])
</script>

