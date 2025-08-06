import 'vuetify/styles'
import { VDateInput } from 'vuetify/labs/VDateInput'
import { createVuetify } from 'vuetify'
import { mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  icons: {
    defaultSet: 'mdi',
    sets: {
      mdi,
    },
  },
  components: {
    VDateInput,
  },
})
