<script setup>
import { reactive, watch, nextTick } from 'vue'
import { store } from '@/stores/step.js'

// helper
const isActive = (n) => store.step === n

// small directive to toggle "inert/disabled" state for inner controls
// it will:
// - set element.inert when available
// - otherwise set disabled/readOnly/tabindex on focusable elements
const lockDirective = {
  mounted(el, binding) {
    applyLock(el, binding.value)
  },
  updated(el, binding) {
    if (binding.value !== binding.oldValue) applyLock(el, binding.value)
  }
}

function applyLock(el, active) {
  // active === true -> section is active (not locked)
  // we want to lock when active === false
  const shouldLock = !active

  // try the inert attribute first (modern browsers)
  try {
    // inert is boolean: true -> element and children are non-interactive
    el.inert = shouldLock
  } catch (e) {
    // ignore if not supported
  }

  // fallback: disable/readonly and set tabindex for keyboard
  const focusables = el.querySelectorAll('input, textarea, select, button, a, [tabindex]')
  focusables.forEach((node) => {
    if (shouldLock) {
      // store original attributes so we can restore later
      if (node._savedDisabled === undefined) node._savedDisabled = node.disabled
      if (node._savedTabIndex === undefined) node._savedTabIndex = node.getAttribute('tabindex')

      // disable and remove from tab order
      node.disabled = true
      node.setAttribute('tabindex', '-1')

      // inputs: make readonly where disabling would change styling badly (optional)
      if (node.tagName.toLowerCase() === 'input' || node.tagName.toLowerCase() === 'textarea') {
        if (node._savedReadOnly === undefined) node._savedReadOnly = node.readOnly
        node.readOnly = true
      }
    } else {
      // restore
      if (node._savedDisabled !== undefined) node.disabled = node._savedDisabled
      if (node._savedTabIndex !== undefined) {
        if (node._savedTabIndex === null) node.removeAttribute('tabindex')
        else node.setAttribute('tabindex', node._savedTabIndex)
      }
      if (node._savedReadOnly !== undefined) node.readOnly = node._savedReadOnly
    }
  })

  // accessibility hint
  if (shouldLock) el.setAttribute('aria-hidden', 'true')
  else el.removeAttribute('aria-hidden')
}

// register directive for local use in this single-file component
const directives = { inert: lockDirective }

// -------- your formData unchanged --------
const formData = reactive({
  dateOfReceipt: '',
  victim: {
    pesel: '',
    documentType: '',
    documentSeries: '',
    documentNumber: '',
    lastName: '',
    firstName: '',
    birthDate: '',
    birthPlace: '',
    phoneNumber: '',
    address: {
      street: '',
      houseNumber: '',
      apartmentNumber: '',
      zipCode: '',
      country: 'PL',
      voivodeship: ''
    },
    correspondenceAddress: {
      sameAsResidential: false,
      street: '',
      houseNumber: '',
      apartmentNumber: '',
      zipCode: '',
      city: '',
      country: 'PL'
    }
  },
  notifier: {
    pesel: '',
    documentType: '',
    documentSeries: '',
    documentNumber: '',
    firstName: '',
    lastName: '',
    address: {
      street: '',
      houseNumber: '',
      apartmentNumber: '',
      zipCode: '',
      city: ''
    }
  },
  accident: {
    date: '',
    time: '',
    place: '',
    workStartHour: '08:00',
    workEndHour: '16:00',
    injuries: '',
    circumstances: '',
    firstAidGranted: false,
    firstAidPlace: '',
    proceedingAuthority: '',
    machineInvolved: false,
    machineName: '',
    machineCompliant: false,
    machineRegistry: false
  },
  witnesses: [
    { firstName: '', lastName: '', address: '' },
    { firstName: '', lastName: '', address: '' }
  ],
  attachments: {
    medicalRecord: false,
    prosecutorDecision: false,
    deathCertificate: false,
    other: false,
    otherDescription: ''
  },
  submission: {
    documentList: '',
    receiptMethod: 'post',
    date: '',
    signature: ''
  }
})
</script>

<template>
  <div class="bg-white p-8 rounded-lg shadow-lg mx-auto">

    <div class="border-b pb-4 mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Zawiadomienie o wypadku (ZUS EWYP)</h2>
      <div class="text-sm text-gray-500">
        Data wpływu:
        <input
          type="date"
          v-model="formData.dateOfReceipt"
          class="border rounded p-1"
        >
      </div>
    </div>

    <!-- SECTION I -->
    <section
      class="mb-8 rounded-lg p-4 transition-all relative"
      :class="isActive(1) ? 'ring-4 ring-blue-400 bg-blue-50' : 'opacity-60'"
      v-inert="isActive(1)"
      v-bind="$attrs"
    >
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        I. Dane osoby poszkodowanej
      </h3>

      <!-- overlay that blocks pointer events when locked but still allows scrolling of parent -->
      <div v-if="!isActive(1)" class="absolute inset-0 z-10" style="background: transparent;"></div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">PESEL</label>
          <input v-model="formData.victim.pesel" type="text"
                 class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Numer telefonu</label>
          <input v-model="formData.victim.phoneNumber" type="tel"
                 class="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Rodzaj dokumentu</label>
          <select v-model="formData.victim.documentType" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
            <option value="dowod_osobisty">Dowód osobisty</option>
            <option value="paszport">Paszport</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Seria</label>
          <input v-model="formData.victim.documentSeries" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Numer</label>
          <input v-model="formData.victim.documentNumber" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nazwisko</label>
          <input v-model="formData.victim.lastName" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border uppercase">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Imię</label>
          <input v-model="formData.victim.firstName" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border uppercase">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data urodzenia</label>
          <input v-model="formData.victim.birthDate" type="date" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Miejsce urodzenia</label>
          <input v-model="formData.victim.birthPlace" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border uppercase">
        </div>
      </div>

      <h4 class="text-md font-medium text-gray-800 mt-4 mb-2">Adres zamieszkania</h4>
      <div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-2">
        <div class="md:col-span-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Ulica</label>
          <input v-model="formData.victim.address.street" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div class="md:col-span-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nr domu</label>
          <input v-model="formData.victim.address.houseNumber" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div class="md:col-span-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nr lokalu</label>
          <input v-model="formData.victim.address.apartmentNumber" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Kod pocztowy</label>
          <input v-model="formData.victim.address.zipCode" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">Nazwa państwa (jeśli inne niż Polska)</label>
          <input v-model="formData.victim.address.country" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>
    </section>

    <!-- SECTION II -->
    <section
      class="mb-8 rounded-lg p-4 transition-all relative"
      :class="isActive(2) ? 'ring-4 ring-blue-400 bg-blue-50' : 'opacity-60'"
      v-inert="isActive(2)"
    >
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        II. Informacje o wypadku
      </h3>

      <div v-if="!isActive(2)" class="absolute inset-0 z-10" style="background: transparent;"></div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data wypadku</label>
          <input v-model="formData.accident.date" type="date" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Godzina</label>
          <input v-model="formData.accident.time" type="time" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Planowane rozpoczęcie pracy</label>
          <input v-model="formData.accident.workStartHour" type="time" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Planowane zakończenie pracy</label>
          <input v-model="formData.accident.workEndHour" type="time" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Rodzaj doznanych urazów</label>
        <textarea v-model="formData.accident.injuries" rows="3" class="w-full border-gray-300 rounded-md shadow-sm p-2 border"></textarea>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Szczegółowy opis okoliczności, miejsca i przyczyn wypadku</label>
        <textarea v-model="formData.accident.circumstances" rows="6" class="w-full border-gray-300 rounded-md shadow-sm p-2 border"></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-4">
        <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700">Czy udzielono pierwszej pomocy?</label>
          <div class="flex gap-4">
            <label class="flex items-center"><input type="radio" :value="true" v-model="formData.accident.firstAidGranted" class="mr-2"> TAK</label>
            <label class="flex items-center"><input type="radio" :value="false" v-model="formData.accident.firstAidGranted" class="mr-2"> NIE</label>
          </div>
        </div>
        <div v-if="formData.accident.firstAidGranted">
           <label class="block text-sm font-medium text-gray-700 mb-1">Nazwa i adres placówki</label>
           <input v-model="formData.accident.firstAidPlace" type="text" class="w-full border-gray-300 rounded-md shadow-sm p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-4">
         <div class="flex items-center gap-4">
          <label class="text-sm font-medium text-gray-700">Wypadek przy obsłudze maszyn?</label>
          <div class="flex gap-4">
            <label class="flex items-center"><input type="radio" :value="true" v-model="formData.accident.machineInvolved" class="mr-2"> TAK</label>
            <label class="flex items-center"><input type="radio" :value="false" v-model="formData.accident.machineInvolved" class="mr-2"> NIE</label>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION III -->
    <section
      class="mb-8 rounded-lg p-4 transition-all relative"
      :class="isActive(3) ? 'ring-4 ring-blue-400 bg-blue-50' : 'opacity-60'"
      v-inert="isActive(3)"
    >
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        III. Załączniki i Oświadczenie
      </h3>

      <div v-if="!isActive(3)" class="absolute inset-0 z-10" style="background: transparent;"></div>

      <div class="space-y-2 mb-6">
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.medicalRecord" class="mr-2"> Kserokopia karty informacyjnej ze szpitala</label>
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.prosecutorDecision" class="mr-2"> Kserokopia postanowienia prokuratury</label>
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.other" class="mr-2"> Inne dokumenty</label>
        <input v-if="formData.attachments.other" v-model="formData.attachments.otherDescription" type="text" placeholder="Wpisz jakie..."
               class="ml-6 w-1/2 border-gray-300 rounded-md shadow-sm p-1 border">
      </div>

      <div class="bg-gray-50 p-4 rounded-md">
        <h4 class="font-bold mb-2">Oświadczenie</h4>
        <p class="text-sm text-gray-600 mb-4">Oświadczam, że dane zawarte w zawiadomieniu podaję zgodnie z prawdą, co potwierdzam złożonym podpisem.</p>
        <div class="flex justify-between items-end">
            <div>
                <label class="block text-sm font-medium text-gray-700">Data</label>
                <input v-model="formData.submission.date" type="date" class="border p-1 rounded">
            </div>
             <div class="w-64 border-b border-black h-8"></div>
        </div>
      </div>
    </section>

    <div class="flex justify-end gap-4 mt-8">
        <button class="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 font-medium">Anuluj</button>
        <button class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium">Generuj PDF</button>
    </div>

  </div>
</template>

<script>
// register local directive so template v-inert works
export default {
  directives: {}
}
</script>

<style>
/* nothing needed — overlay div handles pointer blocking */
</style>
