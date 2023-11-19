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
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'
import InputSwitch from 'primevue/inputswitch';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';
import Row from 'primevue/row';
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.use(ToastService)

app.component('Button', Button)
app.component('Dropdown', Dropdown)
app.component('Menubar', Menubar)
app.component('Card', Card)
app.component('Divider', Divider)
app.component('InputSwitch', InputSwitch)
app.component('InputText', InputText)
app.component('Password', Password)
app.component('Toast', Toast)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('Row', Row)

app.mount('#app')

