<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  loading: boolean
}>()

const emit = defineEmits<{
  search: [query: string]
  clear: []
}>()

const query = ref('')
const isFocused = ref(false)

function handleSearch() {
  if (query.value.trim()) {
    emit('search', query.value)
  }
}

function handleClear() {
  query.value = ''
  emit('clear')
}

function handleSuggestionClick(suggestion: string) {
  query.value = suggestion
  emit('search', suggestion)
}
</script>

<template>
  <div class="search-hero">
    <div class="hero-content">
      <h1>Sök i vår frågebank</h1>
      <p class="subtitle">Utforska insikter från Sveriges ledande ungdomsanalyser</p>
      
      <div class="search-box-container">
        <div class="search-box" :class="{ 'is-focused': isFocused }">
          <div class="input-wrapper">
            <span class="search-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            </span>
            <input 
              v-model="query" 
              @keyup.enter="handleSearch"
              @focus="isFocused = true"
              @blur="isFocused = false"
              type="text" 
              placeholder="Vad vill du veta om unga idag?" 
              class="search-input"
            />
            <button v-if="query" @click="handleClear" class="clear-btn" title="Rensa sökning">✕</button>
          </div>
          <button @click="handleSearch" class="search-btn" :disabled="loading">
            <span v-if="loading" class="loader"></span>
            <span v-else>Sök</span>
          </button>
        </div>
        <div class="search-suggestions" v-if="!query">
          <span>Populära sökningar:</span>
          <button @click="handleSuggestionClick('Sociala medier')" class="suggestion-pill">Sociala medier</button>
          <button @click="handleSuggestionClick('Psykisk hälsa')" class="suggestion-pill">Psykisk hälsa</button>
          <button @click="handleSuggestionClick('Framtidstro')" class="suggestion-pill">Framtidstro</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-hero {
  text-align: center;
  margin-bottom: 4rem;
  position: relative;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 3rem;
  color: #00205b;
  margin-bottom: 1rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.subtitle {
  color: #555;
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  font-weight: 400;
  opacity: 0.9;
}

.search-box-container {
  max-width: 720px;
  margin: 0 auto;
}

.search-box {
  display: flex;
  background: white;
  padding: 6px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 32, 91, 0.08);
  border: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.search-box.is-focused {
  border-color: rgba(227, 0, 79, 0.3);
  box-shadow: 0 8px 30px rgba(227, 0, 79, 0.15);
  transform: translateY(-2px);
}

.input-wrapper {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  padding-left: 16px;
}

.search-icon {
  color: #9ca3af;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 16px 12px;
  font-size: 1.1rem;
  border: none;
  outline: none;
  background: transparent;
  color: #1f2937;
}

.search-input::placeholder {
  color: #9ca3af;
}

.clear-btn {
  margin-right: 8px;
  background: #f3f4f6;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.search-btn {
  background-color: #e3004f;
  color: white;
  border: none;
  padding: 0 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
}

.search-btn:hover {
  background-color: #c40042;
  transform: translateY(-1px);
}

.search-btn:disabled {
  background-color: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.search-suggestions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  font-size: 0.9rem;
  color: #6b7280;
}

.suggestion-pill {
  background: white;
  border: 1px solid #e5e7eb;
  padding: 6px 14px;
  border-radius: 20px;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.85rem;
}

.suggestion-pill:hover {
  border-color: #e3004f;
  color: #e3004f;
  background: rgba(227, 0, 79, 0.02);
}

.loader {
  width: 18px;
  height: 18px;
  border: 2px solid #ffffff;
  border-bottom-color: transparent;
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
