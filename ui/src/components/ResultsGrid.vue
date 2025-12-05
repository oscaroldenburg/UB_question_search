<script setup lang="ts">
import QuestionCard from './QuestionCard.vue'
import type { QuestionItem } from '../api'

defineProps<{
  results: QuestionItem[]
  loading: boolean
}>()

const emit = defineEmits<{
  showDetails: [item: QuestionItem]
}>()

function handleShowDetails(item: QuestionItem) {
  emit('showDetails', item)
}
</script>

<template>
  <div class="results-section">
    <div class="results-header">
      <h2>Sökresultat</h2>
      <span class="count">{{ results.length }} träffar hittades</span>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="ai-loader">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
      <p>Analyserar frågebanken...</p>
    </div>

    <div v-else-if="results.length === 0" class="no-results">
      <div class="empty-state-icon">🔍</div>
      <h3>Inga träffar hittades</h3>
      <p>Prova att söka på något annat eller använd bredare söktermer.</p>
    </div>

    <div v-else class="results-grid">
      <QuestionCard
        v-for="(item, index) in results"
        :key="index"
        :item="item"
        :index="index"
        @show-details="handleShowDetails"
      />
    </div>
  </div>
</template>

<style scoped>
.results-section {
  animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.results-header h2 {
  color: #111827;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.count {
  color: #6b7280;
  font-size: 0.95rem;
  font-weight: 500;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.ai-loader {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 1rem;
}

.dot {
  width: 10px;
  height: 10px;
  background-color: #e3004f;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.03);
}

.empty-state-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
