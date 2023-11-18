import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import Menubar from 'primevue/menubar'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import 'primevue/resources/themes/soho-dark/theme.css' // or any theme of your choice
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import InputSwitch from 'primevue/inputswitch';

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)

app.component('Button', Button)
app.component('Dropdown', Dropdown)
app.component('Menubar', Menubar)
app.component('Card', Card)
app.component('Divider', Divider)
app.component('InputSwitch', InputSwitch)

app.mount('#app')
