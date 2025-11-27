<script setup lang="ts">
import { ref } from 'vue'
import { searchQuestions } from '../api'
import SearchBox from '../components/SearchBox.vue'
import ResultsGrid from '../components/ResultsGrid.vue'
import QuestionModal from '../components/QuestionModal.vue'
import logo from '../assets/UB_logo.webp'

interface QuestionItem {
  question: string
  category?: string
  year?: number
  Answer_alternatives?: string[]
  [key: string]: any
}

const loading = ref(false)
const results = ref<QuestionItem[]>([])
const hasSearched = ref(false)
const selectedItem = ref<QuestionItem | null>(null)
const isModalOpen = ref(false)

async function handleSearch(query: string) {
  loading.value = true
  hasSearched.value = true
  results.value = []

  try {
    const data = await searchQuestions(query)
    results.value = data.items || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function handleClear() {
  results.value = []
  hasSearched.value = false
}

function handleShowDetails(item: QuestionItem) {
  selectedItem.value = item
  isModalOpen.value = true
}

function handleCloseModal() {
  isModalOpen.value = false
  selectedItem.value = null
}
</script>

<template>
  <div class="page-container">
    <header class="header">
      <div class="logo-area">
        <img :src="logo" alt="Ungdomsbarometern Logo" class="logo-image" style="max-width: 150px" />
      </div>
    </header>

    <main class="main-content">
      <SearchBox 
        :loading="loading"
        @search="handleSearch"
        @clear="handleClear"
      />

      <ResultsGrid
        v-if="hasSearched"
        :results="results"
        :loading="loading"
        @show-details="handleShowDetails"
      />
    </main>

    <QuestionModal
      :item="selectedItem"
      :is-open="isModalOpen"
      @close="handleCloseModal"
    />
  </div>
</template>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f4f6f8;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #1a1a1a;
}

.header {
  background-color: #ffffff;
  padding: 1.25rem 2rem;
  border-bottom: 1px solid rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.9);
}

.logo-text {
  font-weight: 800;
  font-size: 1.25rem;
  letter-spacing: -0.02em;
  color: #00205b;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 4rem 1.5rem;
}
</style>
