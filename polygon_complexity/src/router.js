import { createRouter, createWebHistory } from 'vue-router';
import Login from './views/Login.vue';
import Home1 from './views/Home1.vue';
import Select from './views/Select.vue';
import Upload from './views/Upload.vue';
import Draw from './views/Draw.vue';
import DownsamplingBoundaryDetails from './views/DownsamplingBoundaryDetails.vue';
import DownsamplingAreaDetails from './views/DownsamplingAreaDetails.vue';
import BoundaryDetails from './views/BoundaryDetails.vue';
import TriangulationDetails from './views/TriangulationDetails.vue';
import EntropyDetails from './views/EntropyDetails.vue';
import MatDetails from './views/MatDetails.vue';
import EdfDetails from './views/EdfDetails.vue';
import WeightedDetails from './views/WeightedDetails.vue';
import TheoryDownsampling from './views/TheoryDownsampling.vue';
import TheoryBoundary from './views/TheoryBoundary.vue';
import TheoryTriangulation from'./views/TheoryTriangulation.vue';
import TheoryEntropy from './views/TheoryEntropy.vue';
import TheorySkeleton from './views/TheorySkeleton.vue';
import TheoryWeighted from './views/TheoryWeighted.vue';
import About from './views/About.vue';
import SystemDescription from './views/SystemDescription.vue';
import System from './views/System.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home1',
    component: Home1,
    meta: { requiresAuth: true },
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
  {
    path: '/details/triangulation/:fileName',
    name: 'TriangulationDetails',
    component: TriangulationDetails,
    props: true,
  },
  {
    path: '/details/entropy/:fileName',
    name: 'EntropyDetails',
    component: EntropyDetails,
    props: true,
  },
  {
    path: '/details/mat/:fileName',
    name: 'MatDetails',
    component: MatDetails,
    props: true,
  },
  {
    path: '/details/edf/:fileName',
    name: 'EdfDetails',
    component: EdfDetails,
    props: true,
  },
  {
    path: '/details/weighted/:fileName',
    name: 'WeightedDetails',
    component: WeightedDetails,
    props: true,
  },
  {
    path: '/theory/downsampling',
    name: 'TheroyDownsampling',
    component: TheoryDownsampling,
    props: true,
  },
  {
    path: '/theory/boundary',
    name: 'TheoryBoundary',
    component: TheoryBoundary,
    props: true,
  },
  {
    path: '/theory/triangulation',
    name: 'TheoryTriangulation',
    component: TheoryTriangulation,
    props: true,
  },
  {
    path: '/theory/entropy',
    name: 'TheoryEntropy',
    component: TheoryEntropy,
    props: true,
  },
  {
    path: '/theory/Skeleton',
    name: 'TheorySkeleton',
    component: TheorySkeleton,
    props: true,
  },
  {
    path: '/theory/weighted',
    name: 'TheoryWeighted',
    component: TheoryWeighted,
    props: true,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
    props: true,
  },
  {
    path: '/systemdescription',
    name: 'SystemDescription',
    component: SystemDescription,
    props: true,
  },
  {
    path: '/system',
    name: 'System',
    component: System,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('authenticated') === 'true';

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login'); // 未认证，跳转到登录页面
  } else {
    next(); // 允许访问
  }
});

export default router;