<script setup>
import { reactive } from 'vue'

const formData = reactive({
  victim: {
    fullName: '',
    residence: '',
    idDocument: ''
  },
  accident: {
    date: '',
    time: '',
    plannedWorkStart: '08:00',
    plannedWorkEnd: '16:00'
  },
  workDetails: {
    activities: ''
  },
  description: {
    text: '',
  },
  technical: {
    machineInvolved: false,
    machineDetails: '',
    machineCompliant: '',
    protectionUsed: false,
    protectionDetails: '',
    protectionEffective: '',
    assistance: 'nie dotyczy',
    twoPersonRequirement: ''
  },
  safety: {
    rulesFollowed: true,
    preparedForTask: true,
    trainingCompleted: true,
    riskAssessment: true,
    riskMeasures: ''
  },
  state: {
    sober: true,
    tested: 'nie był badany'
  },
  authorities: {
    investigated: false,
    details: ''
  },
  medical: {
    firstAidDate: '',
    facility: '',
    hospitalization: '',
    diagnosis: '',
    incapacityFrom: '',
    incapacityTo: 'NADAL',
    onLeave: false
  },
  meta: {
    date: '',
    location: ''
  }
})
</script>

<template>
  <div class="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto font-serif">
    <div class="text-center mb-8">
      <h1 class="text-2xl font-bold text-gray-900 uppercase tracking-wide">Zapis Wyjaśnień Poszkodowanego</h1>
    </div>

    <section class="mb-6 space-y-4">
      <div class="grid grid-cols-1 gap-4">
        <div>
          <label class="block text-sm font-semibold text-gray-700">Pan/i (Imię i Nazwisko)</label>
          <input v-model="formData.victim.fullName" type="text" class="w-full border-b border-gray-400 focus:border-black outline-none py-1 bg-transparent">
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700">Zamieszkały/a w</label>
          <input v-model="formData.victim.residence" type="text" class="w-full border-b border-gray-400 focus:border-black outline-none py-1 bg-transparent">
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700">Dokument tożsamości (dowód osobisty lub paszport)</label>
          <input v-model="formData.victim.idDocument" type="text" class="w-full border-b border-gray-400 focus:border-black outline-none py-1 bg-transparent">
        </div>
      </div>
    </section>

    <div class="mb-6 text-sm text-gray-600 italic">
      <p>W związku z wypadkiem, jakiemu uległem/am w dniu <input v-model="formData.accident.date" type="date" class="border-b border-gray-300"> uprzedzony/a o odpowiedzialności karnej za składanie fałszywych zeznań oświadczam, co następuje:</p>
    </div>

    <section class="space-y-6">
      <!-- 1-3 -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label class="block font-bold text-sm">1. Data i godzina wypadku</label>
          <div class="flex gap-2">
            <input v-model="formData.accident.date" type="date" class="border p-1 rounded w-full">
            <input v-model="formData.accident.time" type="time" class="border p-1 rounded w-full">
          </div>
        </div>
        <div>
          <label class="block font-bold text-sm">2. Rozpoczęcie pracy</label>
          <input v-model="formData.accident.plannedWorkStart" type="time" class="border p-1 rounded w-full">
        </div>
        <div>
          <label class="block font-bold text-sm">3. Zakończenie pracy</label>
          <input v-model="formData.accident.plannedWorkEnd" type="time" class="border p-1 rounded w-full">
        </div>
      </div>

      <!-- 4 -->
      <div>
        <label class="block font-bold text-sm mb-2">4. Rodzaj czynności wykonywanych do momentu wypadku</label>
        <textarea v-model="formData.workDetails.activities" rows="4" class="w-full border border-gray-300 rounded p-2 text-sm uppercase"></textarea>
      </div>

      <!-- 5 -->
      <div>
        <label class="block font-bold text-sm mb-2">5. Okoliczności i przyczyny wypadku (opis szczegółowy)</label>
        <textarea v-model="formData.description.text" rows="8" class="w-full border border-gray-300 rounded p-2 text-sm uppercase bg-yellow-50"></textarea>
      </div>

      <!-- 6 -->
      <div class="border-t pt-4">
        <label class="block font-bold text-sm">6. Wypadek powstał podczas obsługi maszyn/urządzeń?</label>
        <div class="flex gap-4 my-2">
            <label><input type="radio" :value="true" v-model="formData.technical.machineInvolved"> TAK</label>
            <label><input type="radio" :value="false" v-model="formData.technical.machineInvolved"> NIE</label>
        </div>
        <div v-if="formData.technical.machineInvolved" class="pl-4 border-l-2 border-gray-200">
            <input v-model="formData.technical.machineDetails" placeholder="Nazwa, typ, data produkcji" class="w-full border-b mb-2 outline-none">
            <input v-model="formData.technical.machineCompliant" placeholder="Czy sprawne i zgodne z zasadami?" class="w-full border-b outline-none">
        </div>
      </div>

      <!-- 7 -->
      <div>
        <label class="block font-bold text-sm">7. Czy były stosowane zabezpieczenia?</label>
        <div class="flex gap-4 my-2">
            <label><input type="radio" :value="true" v-model="formData.technical.protectionUsed"> TAK</label>
            <label><input type="radio" :value="false" v-model="formData.technical.protectionUsed"> NIE</label>
            <label><input type="radio" value="na" v-model="formData.technical.protectionUsed"> Nie dotyczy</label>
        </div>
         <div v-if="formData.technical.protectionUsed === true" class="pl-4 border-l-2 border-gray-200">
            <input v-model="formData.technical.protectionDetails" placeholder="Rodzaj środków (buty, kask...)" class="w-full border-b mb-2 outline-none">
            <input v-model="formData.technical.protectionEffective" placeholder="Czy właściwe i sprawne?" class="w-full border-b outline-none">
        </div>
      </div>

      <!-- 9 & 10 & 11 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="flex items-center justify-between border p-2 rounded">
            <span class="text-sm font-bold">9. Przestrzegałem zasad BHP?</span>
            <div class="flex gap-2">
                <label class="cursor-pointer"><input type="radio" :value="true" v-model="formData.safety.rulesFollowed"> TAK</label>
                <label class="cursor-pointer"><input type="radio" :value="false" v-model="formData.safety.rulesFollowed"> NIE</label>
            </div>
        </div>
        <div class="flex items-center justify-between border p-2 rounded">
            <span class="text-sm font-bold">10. Posiadam przygotowanie?</span>
            <div class="flex gap-2">
                <label class="cursor-pointer"><input type="radio" :value="true" v-model="formData.safety.preparedForTask"> TAK</label>
                <label class="cursor-pointer"><input type="radio" :value="false" v-model="formData.safety.preparedForTask"> NIE</label>
            </div>
        </div>
         <div class="flex items-center justify-between border p-2 rounded md:col-span-2">
            <span class="text-sm font-bold">11. Szkolenie BHP?</span>
            <div class="flex gap-2">
                <label class="cursor-pointer"><input type="radio" :value="true" v-model="formData.safety.trainingCompleted"> TAK</label>
                <label class="cursor-pointer"><input type="radio" :value="false" v-model="formData.safety.trainingCompleted"> NIE</label>
            </div>
        </div>
      </div>

      <!-- 12 -->
      <div class="border-t pt-4">
        <label class="block font-bold text-sm">12. Stan trzeźwości</label>
        <div class="flex flex-col gap-2 mt-2">
             <div class="flex gap-4">
                 <span class="text-sm">W chwili wypadku byłem:</span>
                <label><input type="radio" :value="true" v-model="formData.state.sober"> Trzeźwy</label>
                <label><input type="radio" :value="false" v-model="formData.state.sober"> Nietrzeźwy</label>
            </div>
            <select v-model="formData.state.tested" class="border p-1 w-full mt-1">
                <option value="nie był badany">Nie był badany</option>
                <option value="policja">Badany przez Policję</option>
                <option value="lekarz">Badany przy pomocy lekarskiej</option>
            </select>
        </div>
      </div>

      <!-- 14 -->
      <div class="border-t pt-4 bg-gray-50 p-4 rounded">
          <h4 class="font-bold text-sm mb-2">14. Pierwsza pomoc</h4>
          <div class="grid grid-cols-1 gap-2 text-sm">
              <div class="flex items-center gap-2">
                  <span>Data udzielenia:</span>
                  <input type="date" v-model="formData.medical.firstAidDate" class="border p-1">
              </div>
              <div class="flex flex-col">
                  <span>Placówka:</span>
                  <input type="text" v-model="formData.medical.facility" class="border p-1 uppercase">
              </div>
              <div class="flex flex-col">
                  <span>Rozpoznanie (wg dokumentacji):</span>
                  <input type="text" v-model="formData.medical.diagnosis" class="border p-1 uppercase font-bold text-red-800">
              </div>
               <div class="flex items-center gap-2">
                  <span>Niezdolność do pracy od:</span>
                  <input type="date" v-model="formData.medical.incapacityFrom" class="border p-1">
                  <span>do:</span>
                  <input type="text" v-model="formData.medical.incapacityTo" class="border p-1 w-24">
              </div>
          </div>
      </div>

    </section>

    <div class="mt-8 pt-8 border-t-2 border-black flex justify-between items-center">
        <div class="text-center">
            <input v-model="formData.meta.date" type="date" class="block mb-1">
            <input v-model="formData.meta.location" type="text" placeholder="Miejscowość" class="block text-center border-b border-black outline-none">
            <span class="text-xs text-gray-500">(Miejscowość i data)</span>
        </div>
        <div class="text-center mt-6">
            <div class="w-48 border-b border-dotted border-black h-8"></div>
            <span class="text-xs text-gray-500">(Podpis poszkodowanego)</span>
        </div>
    </div>
  </div>
</template>

