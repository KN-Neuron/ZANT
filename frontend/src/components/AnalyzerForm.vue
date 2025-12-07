<script setup>
import { ref, reactive, computed } from 'vue'

const zawiadomienieFile = ref(null)
const wyjasnieniaFile = ref(null)
const isLoading = ref(false)
const result = ref(null)
const error = ref(null)

// Reaktywny obiekt formularza - to co user może edytować i co pójdzie do PDF
const kartaData = reactive({
  // I. PŁATNIK
  platnik_nazwa: '',
  platnik_adres: '',
  platnik_nip: '',
  platnik_dowod_rodzaj: 'Dowód osobisty',
  platnik_dowod_numer: '',

  // II. POSZKODOWANY
  poszkodowany_nazwa: '',
  poszkodowany_pesel: '',
  poszkodowany_dowod_rodzaj: 'Dowód osobisty',
  poszkodowany_dowod_numer: '',
  poszkodowany_urodzenie: '',
  poszkodowany_adres: '',
  tytul_ubezpieczenia: '',

  // III. WYPADEK
  wypadek_zgloszenie: '',
  wypadek_okolicznosci: '',
  wypadek_przyczyna_bezp: '',
  wypadek_przyczyna_posr: '',
  swiadek_1: '',
  swiadek_2: ''
})

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
    const response = await fetch('/raport-wypadku/api/analyze/', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.error || 'Błąd serwera')
    }

    const data = await response.json()
    result.value = data

    // Wypełniamy formularz danymi z AI
    populateForm(data)

  } catch (e) {
    console.error(e)
    error.value = e.message
  } finally {
    isLoading.value = false
  }
}

const statusClass = computed(() => {
  const status = result.value?.analiza_ai?.status
  if (!status) return 'bg-gray-100 text-gray-800 border-gray-300'

  switch (status) {
    case 'Do akceptacji':
      return 'bg-green-100 text-green-800 border-green-300'
    case 'Do odrzucenia':
      return 'bg-red-100 text-red-800 border-red-300'
    case 'Do weryfikacji ręcznej':
    default:
      return 'bg-orange-100 text-orange-800 border-orange-300'
  }
})

const statusIcon = computed(() => {
    const status = result.value?.analiza_ai?.status
    switch (status) {
        case 'Do akceptacji': return '✅'
        case 'Do odrzucenia': return '⛔'
        default: return '⚠️'
    }
})
// ------------------------------------

const populateForm = (data) => {
  const p = data.dane_wniosku?.poszkodowany || {}
  const info = data.dane_wniosku?.informacje_o_wypadku || {}
  const ai = data.analiza_ai || {}

  // II. Poszkodowany
  kartaData.poszkodowany_nazwa = `${p.imie || ''} ${p.nazwisko || ''}`.trim()
  kartaData.poszkodowany_pesel = p.pesel || ''
  kartaData.poszkodowany_adres = p.adres_zamieszkania || ''
  kartaData.poszkodowany_urodzenie = p.data_urodzenia || ''
  // Próba wyciągnięcia numeru dowodu z pola seria_dokumentu
  if(p.seria_dokumentu) kartaData.poszkodowany_dowod_numer = p.seria_dokumentu

  // III. Okoliczności
  // Priorytet ma uzasadnienie wygenerowane przez AI (jeśli jest), bo jest sformatowane prawniczo
  let opis = ai.proponowana_tresc_uzasadnienia
    ? ai.proponowana_tresc_uzasadnienia
    : (info.opis || '')

  // Doklejamy urazy jeśli nie są w opisie
  if (info.urazy && !opis.includes(info.urazy)) {
      opis += `\n\nStwierdzone urazy: ${info.urazy}`
  }

  kartaData.wypadek_okolicznosci = opis

  // Sugestia przyczyny
  if (ai.szansa_przyczyny_zewnetrznej > 0.6) {
      kartaData.wypadek_przyczyna_bezp = "Przyczyna zewnętrzna (zgodnie z analizą zdarzenia)"
  }
}

const downloadPdf = async () => {
  try {
    const response = await fetch('/raport-wypadku/api/generate-pdf/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(kartaData)
    })

    if (!response.ok) throw new Error('Błąd generowania PDF')

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `Karta_Wypadku_${kartaData.poszkodowany_nazwa || 'Draft'}.pdf`
    document.body.appendChild(link)
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    alert("Nie udało się pobrać PDF: " + e.message)
  }
}
</script>

<template>
  <div class="main-container">
    <h2 class="app-title">ZANT - Analizator Wypadków</h2>

    <!-- Sekcja Upload -->
    <div class="upload-section">
      <div class="input-row">
        <label>1. Zawiadomienie (PDF):</label>
        <input type="file" @change="handleZawiadomienieChange" accept=".pdf,.jpg,.jpeg,.png" />
      </div>
      <div class="input-row">
        <label>2. Wyjaśnienia (Opcjonalnie):</label>
        <input type="file" @change="handleWyjasnieniaChange" accept=".pdf,.jpg,.jpeg,.png" />
      </div>
      <button @click="submitForm" :disabled="isLoading" class="btn-primary">
        {{ isLoading ? 'Analizowanie...' : 'Przeanalizuj Dokumenty' }}
      </button>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>

    <div v-if="result" class="workspace">

      <!-- LEWA STRONA: ANALIZA AI (Zawsze widoczna) -->
      <div class="ai-panel">
        <h3>Analiza AI</h3>

        <div class="mb-6 p-4 rounded-lg border-2 text-center shadow-sm" :class="statusClass">
            <span class="block text-2xl mb-1">{{ statusIcon }}</span>
            <span class="block font-bold text-lg uppercase tracking-wide">
                {{ result.analiza_ai.status }}
            </span>
        </div>

        <div class="score-grid">
          <div class="score-card" :class="{high: result.analiza_ai.szansa_uwzglednienia_ze_byl_nagly > 0.6}">
            <span class="label">Nagłość</span>
            <span class="value">{{ (result.analiza_ai.szansa_uwzglednienia_ze_byl_nagly * 100).toFixed(0) }}%</span>
          </div>
          <div class="score-card" :class="{high: result.analiza_ai.szansa_ze_stal_sie_podczas_pracy > 0.6}">
            <span class="label">Związek z pracą</span>
            <span class="value">{{ (result.analiza_ai.szansa_ze_stal_sie_podczas_pracy * 100).toFixed(0) }}%</span>
          </div>
          <div class="score-card" :class="{high: result.analiza_ai.szansa_przyczyny_zewnetrznej > 0.6}">
            <span class="label">Przycz. zewn.</span>
            <span class="value">{{ (result.analiza_ai.szansa_przyczyny_zewnetrznej * 100).toFixed(0) }}%</span>
          </div>
          <div class="score-card" :class="{high: result.analiza_ai.szansa_urazu_lub_smierci > 0.6}">
            <span class="label">Uraz</span>
            <span class="value">{{ (result.analiza_ai.szansa_urazu_lub_smierci * 100).toFixed(0) }}%</span>
          </div>
        </div>

        <div class="ai-reasoning">
          <strong>Uzasadnienie modelu:</strong>
          <p>{{ result.analiza_ai.reasoning }}</p>
        </div>
      </div>

      <!-- PRAWA STRONA: EDYCJA I GENEROWANIE PDF -->
      <div class="form-panel">
        <div class="form-header">
          <h3>Karta Wypadku (Edycja)</h3>
          <button @click="downloadPdf" class="btn-pdf">⬇ Pobierz PDF</button>
        </div>

        <div class="paper-form">
          <!-- I. PŁATNIK -->
          <div class="section-block">
            <h4>I. DANE PŁATNIKA SKŁADEK</h4>
            <div class="field">
              <label>Imię i nazwisko / Nazwa:</label>
              <input v-model="kartaData.platnik_nazwa" type="text" placeholder="Wpisz nazwę płatnika..." />
            </div>
            <div class="field">
              <label>Adres siedziby:</label>
              <input v-model="kartaData.platnik_adres" type="text" />
            </div>
            <div class="field-row">
              <div class="field">
                <label>NIP:</label>
                <input v-model="kartaData.platnik_nip" type="text" />
              </div>
              <div class="field">
                <label>Nr dowodu/paszportu:</label>
                <input v-model="kartaData.platnik_dowod_numer" type="text" />
              </div>
            </div>
          </div>

          <!-- II. POSZKODOWANY -->
          <div class="section-block">
            <h4>II. DANE POSZKODOWANEGO</h4>
            <div class="field">
              <label>Imię i nazwisko:</label>
              <input v-model="kartaData.poszkodowany_nazwa" type="text" />
            </div>
            <div class="field-row">
              <div class="field">
                <label>PESEL:</label>
                <input v-model="kartaData.poszkodowany_pesel" type="text" />
              </div>
              <div class="field">
                <label>Nr dowodu:</label>
                <input v-model="kartaData.poszkodowany_dowod_numer" type="text" />
              </div>
            </div>
            <div class="field">
              <label>Adres zamieszkania:</label>
              <input v-model="kartaData.poszkodowany_adres" type="text" />
            </div>
            <div class="field">
              <label>Tytuł ubezpieczenia:</label>
              <input v-model="kartaData.tytul_ubezpieczenia" type="text" />
            </div>
          </div>

          <!-- III. WYPADEK -->
          <div class="section-block">
            <h4>III. INFORMACJE O WYPADKU</h4>
            <div class="field">
              <label>Data zgłoszenia i zgłaszający:</label>
              <input v-model="kartaData.wypadek_zgloszenie" type="text" />
            </div>
            <div class="field">
              <label>Okoliczności i przyczyny (opis):</label>
              <textarea v-model="kartaData.wypadek_okolicznosci" rows="6"></textarea>
            </div>
            <div class="field">
              <label>Przyczyna bezpośrednia:</label>
              <input v-model="kartaData.wypadek_przyczyna_bezp" type="text" />
            </div>
            <div class="field">
              <label>Przyczyna pośrednia:</label>
              <input v-model="kartaData.wypadek_przyczyna_posr" type="text" />
            </div>
            <div class="field">
              <label>Świadek 1:</label>
              <input v-model="kartaData.swiadek_1" type="text" />
            </div>
             <div class="field">
              <label>Świadek 2:</label>
              <input v-model="kartaData.swiadek_2" type="text" />
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.main-container { max-width: 1200px; margin: 0 auto; font-family: 'Inter', sans-serif; color: #333; }
.app-title { text-align: center; margin-bottom: 20px; color: #2c3e50; }

/* UPLOAD SECTION */
.upload-section {
  background: #fff; padding: 20px; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; gap: 20px; align-items: flex-end; flex-wrap: wrap; margin-bottom: 30px;
}
.input-row { display: flex; flex-direction: column; flex: 1; min-width: 250px; }
.input-row label { font-size: 0.9rem; margin-bottom: 5px; font-weight: 600; }
.btn-primary {
  background: #00bd7e; color: white; border: none; padding: 10px 20px;
  border-radius: 6px; cursor: pointer; font-weight: bold; height: 42px;
}
.btn-primary:hover { background: #009e69; }
.error-msg { color: white; background: #e74c3c; padding: 10px; border-radius: 6px; margin-bottom: 20px; }

/* WORKSPACE LAYOUT */
.workspace { display: grid; grid-template-columns: 350px 1fr; gap: 30px; align-items: start; }
@media (max-width: 900px) { .workspace { grid-template-columns: 1fr; } }

/* AI PANEL (LEFT) */
.ai-panel { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; position: sticky; top: 20px; }
.ai-panel h3 { margin-bottom: 15px; color: #2c3e50; border-bottom: 2px solid #00bd7e; padding-bottom: 5px; display: inline-block; }
.score-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }
.score-card {
  background: #fff; padding: 10px; border-radius: 6px; text-align: center;
  border: 1px solid #ddd; display: flex; flex-direction: column;
}
.score-card.high { border-color: #00bd7e; background-color: #e8f5e9; }
.score-card .label { font-size: 0.75rem; color: #666; }
.score-card .value { font-size: 1.2rem; font-weight: bold; color: #2c3e50; }
.ai-reasoning { font-size: 0.9rem; line-height: 1.5; background: #fff; padding: 15px; border-radius: 6px; border: 1px solid #ddd; }

/* FORM PANEL (RIGHT) */
.form-panel { background: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden; }
.form-header {
  background: #2c3e50; color: white; padding: 15px 20px;
  display: flex; justify-content: space-between; align-items: center;
}
.btn-pdf { background: #e74c3c; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: bold; }
.btn-pdf:hover { background: #c0392b; }

.paper-form { padding: 30px; background: #fafafa; }
.section-block { margin-bottom: 25px; background: #fff; padding: 20px; border: 1px solid #eee; border-radius: 4px; }
.section-block h4 { font-size: 0.85rem; text-transform: uppercase; color: #7f8c8d; border-bottom: 1px solid #eee; padding-bottom: 8px; margin-bottom: 15px; letter-spacing: 1px; }

.field { margin-bottom: 12px; }
.field label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 4px; color: #555; }
.field input, .field textarea {
  width: 100%; padding: 8px 12px; border: 1px solid #ccc; border-radius: 4px;
  font-size: 0.95rem; font-family: inherit;
}
.field input:focus, .field textarea:focus { border-color: #00bd7e; outline: none; background: #fff; }
.field-row { display: flex; gap: 15px; }
.field-row .field { flex: 1; }
</style>