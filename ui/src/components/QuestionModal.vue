<script setup lang="ts">
import { onMounted, onUnmounted, watch, ref } from 'vue'
import { getQuestion, type QuestionItem } from '../api'

const searching = ref(false)
const referenceQuestion = ref<QuestionItem | null>(null)

const props = defineProps<{
  item: QuestionItem | null
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
  openReference: [item: QuestionItem]
}>()

function handleClose() {
  emit('close')
}

function handleOpenReference() {
  if (referenceQuestion.value) {
    emit('openReference', referenceQuestion.value)
  }
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    handleClose()
  }
}

async function fetchReference(var_name: string) {
  searching.value = true
  referenceQuestion.value = null

  try {
    const data = await getQuestion(var_name)
    referenceQuestion.value = data || null
  } catch (e) {
    console.error(e)
  } finally {
    searching.value = false
  }
}

watch(() => props.item, (newItem) => {
  if (newItem?.refference_used) {
    fetchReference(newItem.refference_used)
  } else {
    referenceQuestion.value = null
  }
}, { immediate: true })

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Transition name="modal">
    <div v-if="isOpen && item" class="modal-overlay" @click.self="handleClose">
      <div class="modal-container">
        <div class="modal-header">
          <h2>Frågedetaljer</h2>
          <button class="close-btn" @click="handleClose" title="Stäng">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="question-section">
            <h3 class="section-title">Fråga</h3>
            <p class="question-text">{{ item.question }}</p>
          </div>

          <div class="metadata-section">
            <div v-if="item.category" class="metadata-item">
              <span class="metadata-label">Kategori:</span>
              <span class="metadata-value">{{ item.category }}</span>
            </div>
            <div v-if="item.year" class="metadata-item">
              <span class="metadata-label">År:</span>
              <span class="metadata-value">{{ item.year }}</span>
            </div>
          </div>

          <div class="metadata-section" v-if="item.refference_used">
            <div v-if="item.refference_used" class="metadata-item">
              <span class="metadata-label">Referensvariabel:</span>
              <span class="metadata-value code-style">{{ item.refference_used }}</span>
            </div>
            <div v-if="searching" class="reference-loading">Laddar referens...</div>
            <div v-else-if="referenceQuestion" class="metadata-item">
              <span class="metadata-label">Referensfråga:</span>
              <p class="reference-question">{{ referenceQuestion.question }}</p>
                  <button class="link-btn" @click="handleOpenReference">
                    Visa referensfråga &rarr;
                  </button>
            </div>
            <div v-else class="metadata-item">
              <span class="metadata-label">Referensfråga:</span>
              <span class="metadata-value">Ingen referens hittades.</span>
            </div>
          </div>

          <div v-if="item.answer_alternatives && item.answer_alternatives.length > 0" class="alternatives-section">
            <h3 class="section-title">Svarsalternativ</h3>
            <ul class="alternatives-list">
              <li v-for="(alternative, index) in item.answer_alternatives" :key="index" class="alternative-item">
                {{ alternative }}
              </li>
            </ul>
          </div>

          <!-- <div class="info-section">
            <h3 class="section-title">Ytterligare information</h3>
            <p class="info-placeholder">Här kan du lägga till mer information om frågan, såsom statistik, analys eller relaterade insikter.</p>
          </div> -->
        </div>
        
        <div class="modal-footer">
          <button class="primary-btn" @click="handleClose">Stäng</button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 20px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #00205b;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.2s;
  border-radius: 8px;
}

.close-btn:hover {
  color: #111827;
  background-color: #f3f4f6;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.question-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

.question-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  line-height: 1.6;
  margin: 0;
}

.metadata-section {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f9fafb;
  border-radius: 12px;
}

.metadata-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metadata-item.full-width {
  width: 100%;
}

.reference-container {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.code-style {
  font-family: monospace;
  background: #e5e7eb;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.9rem;
  align-self: flex-start;
}

.reference-preview {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  margin-top: 0.5rem;
}

.reference-question {
  margin: 0 0 0.5rem 0;
  font-size: 0.95rem;
  color: #374151;
  font-style: italic;
}

.link-btn {
  background: none;
  border: none;
  padding: 0;
  color: #e3004f;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.link-btn:hover {
  text-decoration: underline;
}

.metadata-label {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metadata-value {
  font-size: 1rem;
  color: #111827;
  font-weight: 600;
}

.alternatives-section {
  margin-bottom: 2rem;
}

.alternatives-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alternative-item {
  padding: 0.875rem 1rem;
  margin-bottom: 0.5rem;
  background-color: #f9fafb;
  border-radius: 8px;
  border-left: 3px solid #e3004f;
  color: #374151;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.alternative-item:hover {
  background-color: #f3f4f6;
  transform: translateX(4px);
}

.info-section {
  padding: 1.5rem;
  background-color: #fef3c7;
  border-radius: 12px;
  border: 1px solid #fde68a;
}

.info-placeholder {
  margin: 0;
  color: #92400e;
  font-size: 0.9rem;
  line-height: 1.5;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
}

.primary-btn {
  background-color: #e3004f;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-btn:hover {
  background-color: #c40042;
  transform: translateY(-1px);
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>
