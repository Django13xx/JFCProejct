import './assets/main.css'
import '@fortawesome/fontawesome-free/css/all.css';

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'

import axios from 'axios';
import VueCookies from 'vue-cookies';

import router from './router'

// Include CSRF token in your requests
const csrfToken = VueCookies.get('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

const app = createApp(App)

app.use(ElementPlus);

app.use(createPinia())
app.use(router)

app.use(ElementPlus)

app.mount('#app')






