<!-- frontend/src/components/AnalyzerForm.vue -->
<script setup>
import { ref } from 'vue'

const zawiadomienieFile = ref(null)
const wyjasnieniaFile = ref(null)
const isLoading = ref(false)
const result = ref(null)
const error = ref(null)

const handleZawiadomienieChange = (e) => {
  zawiadomienieFile.value = e.target.files[0]
}

const handleWyjasnieniaChange = (e) => {
  wyjasnieniaFile.value = e.target.files[0]
}

const submitForm = async () => {
  if (!zawiadomienieFile.value) {
    alert("Proszę wybrać plik zawiadomienia!")
    return
  }

  isLoading.value = true
  error.value = null
  result.value = null

  const formData = new FormData()
  formData.append('zawiadomienie', zawiadomienieFile.value)

  if (wyjasnieniaFile.value) {
    formData.append('wyjasnienia', wyjasnieniaFile.value)
  }

  try {
    // Uwaga: w developmencie (npm run dev) musisz mieć proxy w vite.config.js
    // albo używać pełnego adresu jeśli Django stoi na 8000
    const response = await fetch('/raport-wypadku/api/analyze/', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.error || 'Błąd serwera')
    }

    result.value = await response.json()
  } catch (e) {
    console.error(e)
    error.value = e.message
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="analyzer-container">
    <h2>ZANT - Analizator Wypadków</h2>

    <div class="form-group">
      <label>1. Zawiadomienie o wypadku (PDF/JPG):</label>
      <input type="file" @change="handleZawiadomienieChange" accept=".pdf,.jpg,.jpeg,.png" />
    </div>

    <div class="form-group">
      <label>2. Wyjaśnienia poszkodowanego (Opcjonalnie):</label>
      <input type="file" @change="handleWyjasnieniaChange" accept=".pdf,.jpg,.jpeg,.png" />
    </div>

    <button @click="submitForm" :disabled="isLoading" class="submit-btn">
      {{ isLoading ? 'Analizowanie...' : 'Przeanalizuj Sprawę' }}
    </button>

    <div v-if="error" class="error-box">
      {{ error }}
    </div>

    <div v-if="result" class="result-box">
      <h3>Wynik Analizy AI</h3>

      <!-- Sekcja Decyzji -->
      <div class="scores">
        <div class="score-item">
          <span>Czy nagły?</span>
          <strong>{{ (result.analiza_ai.szansa_uwzglednienia_ze_byl_nagly * 100).toFixed(0) }}%</strong>
        </div>
        <div class="score-item">
          <span>Związek z pracą?</span>
          <strong>{{ (result.analiza_ai.szansa_ze_stal_sie_podczas_pracy * 100).toFixed(0) }}%</strong>
        </div>
        <div class="score-item">
          <span>Przyczyna zewn.?</span>
          <strong>{{ (result.analiza_ai.szansa_przyczyny_zewnetrznej * 100).toFixed(0) }}%</strong>
        </div>
        <div class="score-item">
          <span>Uraz?</span>
          <strong>{{ (result.analiza_ai.szansa_urazu_lub_smierci * 100).toFixed(0) }}%</strong>
        </div>
      </div>

      <div class="reasoning">
        <h4>Uzasadnienie:</h4>
        <p>{{ result.analiza_ai.reasoning }}</p>
      </div>

      <div class="data-preview">
        <h4>Odczytane dane:</h4>
        <p><strong>Opis:</strong> {{ result.dane_wniosku.informacje_o_wypadku.opis }}</p>
        <p><strong>Urazy:</strong> {{ result.dane_wniosku.informacje_o_wypadku.urazy }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analyzer-container { max-width: 600px; margin: 0 auto; padding: 20px; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
.submit-btn { background-color: #00bd7e; color: white; padding: 10px 20px; border: none; cursor: pointer; font-size: 16px; margin-top: 10px;}
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.result-box { margin-top: 30px; padding: 20px; background: #f4f4f4; border-radius: 8px; color: #333; }
.error-box { margin-top: 20px; color: red; font-weight: bold; }
.scores { display: flex; justify-content: space-between; margin-bottom: 20px; background: #fff; padding: 10px; border-radius: 4px;}
.score-item { display: flex; flex-direction: column; align-items: center; }
.reasoning { background: #e8f5e9; padding: 10px; border-left: 4px solid #00bd7e; margin-bottom: 20px; }
</style>