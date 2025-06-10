import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatTest from '@/views/ChatTest.vue'
import IndexView from '@/views/IndexView.vue'
import ProductDetail from '@/views/ProductDetail.vue'
import Login from '@/views/Login.vue'
import Checkout from '@/views/Checkout.vue'
import OrderHistory from '@/views/OrderHistory.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: IndexView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/chattest',
      name: 'chattest',
      component: ChatTest,
    },
    { path: '/products/:id', component: ProductDetail },
    { path: '/login', component: Login },
    { path: '/checkout', component: Checkout },
    { path: '/orderhistory', component: OrderHistory },
  ],
})

export default router
