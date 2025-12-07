import { reactive } from 'vue'

export const store = reactive({
  step: -1,
  selectedForms: [], // Przechowuje wybrane formularze (np. ['Zawiadomienie', 'Wyjaśnienia'])
  triggerValidation: false // Flaga do uruchamiania walidacji z innego komponentu
})