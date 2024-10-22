<<<<<<< HEAD
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

=======
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

>>>>>>> 9940b710187e10b903004c6d68852d2e6f417ace
export default router;