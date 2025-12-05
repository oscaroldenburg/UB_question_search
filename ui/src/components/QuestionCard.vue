<script setup lang="ts">
import { ref } from 'vue'
import type { QuestionItem } from '../api'

const props = defineProps<{
  item: QuestionItem
  index: number
}>()

const emit = defineEmits<{
  showDetails: [item: QuestionItem]
}>()

const defaultColor = { bg: '#f3f4f6', text: '#4b5563' }

const categoryColors: Record<string, { bg: string; text: string }> = {
  'Samhälle': { bg: '#e0f2fe', text: '#0369a1' },
  'Livsstil': { bg: '#fef3c7', text: '#92400e' },
  'Politik': { bg: '#ede9fe', text: '#5b21b6' },
  'Framtid': { bg: '#d1fae5', text: '#065f46' },
  'Kultur': { bg: '#fce7f3', text: '#9f1239' },
  'Utbildning': { bg: '#dbeafe', text: '#1e40af' },
  'Hälsa': { bg: '#dcfce7', text: '#166534' },
  'Teknologi': { bg: '#e0e7ff', text: '#3730a3' }
}

function getCategoryColor(category?: string): { bg: string; text: string } {
  if (!category) {
    return defaultColor
  }
  return categoryColors[category] || defaultColor
}

function handleShowMore() {
  emit('showDetails', props.item)
}
</script>

<template>
  <div class="result-card" :style="{ animationDelay: `${index * 0.05}s` }">
    <div class="card-content">
      <h3 class="question-text">{{ item.question || 'Fråga saknas' }}</h3>
      
      <div class="category-badge" 
           v-if="item.category"
           :style="{ 
             backgroundColor: getCategoryColor(item.category).bg, 
             color: getCategoryColor(item.category).text 
           }">
        {{ item.category }}
      </div>
    </div>
    
    <div class="card-footer">
      <button class="show-more-btn" @click="handleShowMore">
        Visa mer
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.result-card {
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  animation: fadeIn 0.5s ease-out backwards;
  height: 100%;
}

.result-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 32, 91, 0.08);
  border-color: rgba(227, 0, 79, 0.1);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-text {
  margin: 0;
  color: #111827;
  font-size: 1.15rem;
  line-height: 1.5;
  font-weight: 600;
}

.category-badge {
  align-self: flex-start;
  font-size: 0.75rem;
  padding: 6px 14px;
  border-radius: 20px;
  font-weight: 600;
  letter-spacing: 0.02em;
  text-transform: capitalize;
}

.card-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.show-more-btn {
  background: none;
  border: none;
  color: #e3004f;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: gap 0.2s;
}

.show-more-btn:hover {
  gap: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
