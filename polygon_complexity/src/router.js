import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Select from './views/Select.vue';
import Upload from './views/Upload.vue';
import Draw from './views/Draw.vue';
import DownsamplingBoundaryDetails from './views/DownsamplingBoundaryDetails.vue';
import DownsamplingAreaDetails from './views/DownsamplingAreaDetails.vue';
import BoundaryDetails from './views/BoundaryDetails.vue';

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
  },
  {
    path: '/details/downsampingboundary/:fileName',
    name: 'DownsamplingBoundaryDetails',
    component: DownsamplingBoundaryDetails,
    props: true, 
  },
  {
    path: '/details/downsampingarea/:fileName',
    name: 'DownsamplingAreaDetails',
    component: DownsamplingAreaDetails,
    props: true,
  },
  {
    path: '/details/boundary/:fileName',
    name: 'BoundaryDetails',
    component: BoundaryDetails,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;