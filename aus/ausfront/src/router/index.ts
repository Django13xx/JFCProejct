import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')  
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path:"/help",
      name:"help",
      component: () => import('../views/HelpView.vue')
    },
    {
      path:"/mainPage",
      name:"mainPage",
      component: () => import('../views/MainPageView.vue')
    },
    {
      path:"/teachingDashboard",
      name:"teachingDashboard",
      component: () => import('../views/TeachingDashboardView.vue')
    },
  ]
})

export default router
