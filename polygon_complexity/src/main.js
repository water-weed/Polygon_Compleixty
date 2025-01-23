import { createApp } from 'vue'
import './style.css'
import App from './App.vue';
import router from './router';
import store from './store';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import { Buffer } from "buffer";

const app = createApp(App);

app.use(router);  
app.mount('#app');
app.use(store);
app.use(ElementPlus);
window.Buffer = Buffer;
