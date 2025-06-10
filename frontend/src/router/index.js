import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatTest from '@/views/ChatTest.vue'
import IndexView from '@/views/IndexView.vue'
import ProductDetail from '@/views/ProductDetail.vue'
import Login from '@/views/Login.vue'
import Checkout from '@/views/Checkout.vue'
import CheckoutResult from '@/views/CheckoutResult.vue'
import OrderHistory from '@/views/OrderHistory.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: IndexView },
    { path: '/:category', component: IndexView },
    { path: '/chattest', component: ChatTest },
    { path: '/products/:id', component: ProductDetail },
    { path: '/login', component: Login },
    { path: '/checkout', component: Checkout },
    { path: '/checkoutresult/:order', component: CheckoutResult },
    { path: '/orderhistory', component: OrderHistory },
  ],
})

export default router
