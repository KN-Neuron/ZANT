import { defineStore } from 'pinia'
import { reactive } from 'vue'

export const useFormStore = defineStore('form', () => {
  const data = reactive({
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

  return { data }
})