import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Select from './views/Select.vue';
import Upload from './views/Upload.vue';
import Draw from './views/Draw.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/Select',
    name: 'Select',
    component: Select
  },
  {
    path: '/Upload',
    name: 'Upload',
    component: Upload
  },
  {
    path: '/Draw',
    name: 'Draw',
    component: Draw
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;