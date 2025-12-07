<script setup>
import { useFormStore } from '@/stores/form.js'

const formStore = useFormStore()
const formData = formStore.data

// Brak watcherów - pola są w pełni ręczne i edytowalne
</script>

<template>
  <div class="bg-white p-8 rounded-lg shadow-lg mx-auto">
    <div class="border-b pb-4 mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Zawiadomienie o wypadku (ZUS EWYP)</h2>
      <div class="text-sm text-gray-500">
        Data wpływu:
        <input type="date" v-model="formData.dateOfReceipt" class="border rounded p-1">
      </div>
    </div>

    <!-- SEKCJA I: PŁATNIK -->
    <section class="mb-8 bg-gray-50 rounded-lg p-4 border border-blue-100">
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        I. Dane zgłaszającego (Płatnika składek)
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 bg-white p-3 rounded border border-blue-200">
        <div>
            <label class="block text-sm font-bold text-gray-800 mb-1">NIP</label>
            <input v-model="formData.notifier.nip" type="text" placeholder="np. 1234567890" maxlength="10"
                   class="w-full border-gray-300 rounded-md p-2 border">
        </div>
         <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-600 mb-1">Nazwa firmy</label>
            <input v-model="formData.notifier.businessName" type="text"
                   class="w-full border-gray-300 rounded-md p-2 border">
        </div>
         <div class="md:col-span-3">
            <label class="block text-sm font-medium text-gray-600 mb-1">Kod i nazwa przeważającej działalności (PKD)</label>
            <input v-model="formData.notifier.pkdCode" type="text"
                   class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Imię</label>
          <input v-model="formData.notifier.firstName" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nazwisko</label>
          <input v-model="formData.notifier.lastName" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Rodzaj dokumentu</label>
          <select v-model="formData.notifier.documentType" class="w-full border-gray-300 rounded-md p-2 border">
            <option value="Dowód osobisty">Dowód osobisty</option>
            <option value="Paszport">Paszport</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Seria</label>
          <input v-model="formData.notifier.documentSeries" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Numer</label>
          <input v-model="formData.notifier.documentNumber" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

       <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
         <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Ulica</label>
            <input v-model="formData.notifier.address.street" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nr domu/lokalu</label>
            <input v-model="formData.notifier.address.houseNumber" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Kod pocztowy</label>
            <input v-model="formData.notifier.address.zipCode" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Miejscowość</label>
            <input v-model="formData.notifier.address.city" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
       </div>
    </section>

    <!-- SEKCJA I cz. 2: POSZKODOWANY -->
    <section class="mb-8 bg-gray-50 rounded-lg p-4 border border-blue-100">
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        I cz. 2. Dane osoby poszkodowanej
      </h3>

       <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">PESEL</label>
          <input v-model="formData.victim.pesel" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
          <input v-model="formData.victim.phoneNumber" type="tel" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Imię</label>
          <input v-model="formData.victim.firstName" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nazwisko</label>
          <input v-model="formData.victim.lastName" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

       <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Rodzaj dokumentu</label>
          <select v-model="formData.victim.documentType" class="w-full border-gray-300 rounded-md p-2 border">
            <option value="Dowód osobisty">Dowód osobisty</option>
            <option value="Paszport">Paszport</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Seria</label>
          <input v-model="formData.victim.documentSeries" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Numer</label>
          <input v-model="formData.victim.documentNumber" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <h4 class="text-sm font-bold text-gray-600 mt-4 mb-2">Adres zamieszkania poszkodowanego</h4>
       <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
         <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Ulica</label>
            <input v-model="formData.victim.address.street" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nr domu/lokalu</label>
            <input v-model="formData.victim.address.houseNumber" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Kod pocztowy</label>
            <input v-model="formData.victim.address.zipCode" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
         <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Miejscowość</label>
            <input v-model="formData.victim.address.city" type="text" class="w-full border-gray-300 rounded-md p-2 border">
         </div>
       </div>
    </section>

    <!-- SEKCJA II: WYPADEK -->
    <section class="mb-8 bg-gray-50 rounded-lg p-4 border border-blue-100">
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        II. Informacje o wypadku
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Data wypadku</label>
          <input v-model="formData.accident.date" type="date" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Godzina</label>
          <input v-model="formData.accident.time" type="time" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Planowane rozpoczęcie pracy</label>
          <input v-model="formData.accident.workStartHour" type="time" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Planowane zakończenie pracy</label>
          <input v-model="formData.accident.workEndHour" type="time" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-1">Rodzaj doznanych urazów</label>
        <textarea v-model="formData.accident.injuries" rows="2" placeholder="np. Złamanie otwarte kości piszczelowej lewej..." class="w-full border-gray-300 rounded-md p-2 border"></textarea>
      </div>

      <div class="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
        <label class="block text-sm font-bold text-gray-800 mb-1">
            Szczegółowy opis okoliczności i przyczyn wypadku
            <span class="text-xs font-normal text-gray-500 block">Opisz co robiłeś, co się stało i dlaczego. Asystent pomoże Ci to zweryfikować.</span>
        </label>
        <textarea v-model="formData.accident.circumstances" rows="6" class="w-full border-gray-300 rounded-md p-2 border"></textarea>
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
           <label class="block text-sm font-medium text-gray-700 mb-1">Nazwa placówki medycznej</label>
           <input v-model="formData.accident.firstAidPlace" type="text" class="w-full border-gray-300 rounded-md p-2 border">
        </div>
      </div>

      <div class="mb-4 pt-4 border-t">
          <label class="flex items-center mb-2 font-medium"><input type="checkbox" v-model="formData.accident.machineInvolved" class="mr-2"> Wypadek przy obsłudze maszyn?</label>
          <div v-if="formData.accident.machineInvolved" class="pl-6">
              <label class="block text-sm text-gray-600">Nazwa i typ maszyny</label>
              <input v-model="formData.accident.machineName" type="text" class="w-full border-gray-300 rounded-md p-2 border mb-2">
          </div>
      </div>
    </section>

    <!-- SEKCJA III: ZAŁĄCZNIKI -->
    <section class="mb-8 bg-gray-50 rounded-lg p-4 border border-blue-100">
      <h3 class="text-lg font-semibold text-blue-700 mb-4 border-b border-blue-100 pb-2">
        III. Załączniki (Checklista)
      </h3>
      <div class="space-y-2 mb-6">
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.medicalRecord" class="mr-2"> Kserokopia dokumentacji medycznej</label>
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.prosecutorDecision" class="mr-2"> Notatka policji / Prokuratury</label>
        <label class="flex items-center"><input type="checkbox" v-model="formData.attachments.other" class="mr-2"> Inne (np. szkic sytuacyjny)</label>
      </div>
    </section>
  </div>
</template>