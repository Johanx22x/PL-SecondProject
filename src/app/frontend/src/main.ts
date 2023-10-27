import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

import 'element-plus/dist/index.css'

import router from './router'
import store from './store'

import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { fas } from "@fortawesome/free-solid-svg-icons"
import { fab } from "@fortawesome/free-brands-svg-icons"

library.add(fas, fab);
const app = createApp(App)

app.use(ElementPlus).component("font-awesome-icon", FontAwesomeIcon)
app.use(router)
app.use(store)
app.mount('#app')
