import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import ImageDetection from '../views/ImageDetection.vue'
import RealTimeDetection from '../views/RealTimeDetection.vue'
import LoginPage from '../views/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: { requiresAuth: true }
    },
    {
      path: '/image-detection',
      name: 'image-detection',
      component: ImageDetection,
      meta: { requiresAuth: true }
    },
    {
      path: '/realtime-detection',
      name: 'realtime-detection',
      component: RealTimeDetection,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('loggedIn') === 'true'
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router
