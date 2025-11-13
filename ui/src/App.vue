<script setup lang="js"></script>

<template>
  <div class="app">
    <h1>UB Frågesök</h1>
    <input
      v-model="query"
      @keyup.enter="doSearch"
      placeholder="Sök frågor..."
    />
    <button @click="doSearch">Sök</button>

    <p v-if="loading">Söker...</p>
    <p v-if="!loading && results.length === 0">Inga resultat ännu.</p>

    <ul v-if="results.length">
      <li v-for="item in results" :key="item.id">
        {{ item.question || JSON.stringify(item)}}
      </li>
    </ul>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { searchQuestions } from './api.js'

const query = ref('')
const loading = ref(false)
const results = ref([])

async function doSearch() {
  if (!query.value) return
  loading.value = true

  try {
    const data = await searchQuestions(query.value)
    results.value = data.items
  } finally {
    loading.value = false
  }
}
</script>

<style scoped></style>
