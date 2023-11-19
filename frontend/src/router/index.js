import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import TruckerMetrics from '../views/TruckerMetrics.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/trucker-metrics/:username',
      name: 'TruckerMetrics',
      component: TruckerMetrics,
      props: true
    }
  ]
})

export default router
