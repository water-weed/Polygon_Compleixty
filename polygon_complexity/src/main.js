import { createApp } from 'vue'
import './style.css'
import App from './App.vue';
import router from './router';
import store from './store';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import { Buffer } from "buffer";
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faUpload, faDownload, faPen, faFolderOpen } from '@fortawesome/free-solid-svg-icons';
/*import tippy from 'vue-tippy';
import 'tippy.js/dist/tippy.css'
import 'tippy.js/animations/scale.css'*/
import katex from "katex";
import "katex/dist/katex.min.css";


library.add(faUpload, faDownload, faPen, faFolderOpen);

const app = createApp(App);

app.use(router);  

app.component('font-awesome-icon', FontAwesomeIcon);

/*app.use(tippy,{
    defaultProps:{
        animation: 'scale',
        placement:'bottom',
        //hideOnClick: false,
        //trigger: 'click' ,
        interactive: true,
    } 
});*/

app.mount('#app');
app.use(store);
app.use(ElementPlus);
app.use(katex);
window.Buffer = Buffer;

