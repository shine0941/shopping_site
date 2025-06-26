// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import vuetify from './plugins/vuetify'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import deviceDetector from './plugins/deviceDetector'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)
app.use(deviceDetector)
app.mount('#app')
