import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatTest from '@/views/ChatTest.vue'
import ProductList from '@/views/ProductList.vue'
import ProductDetail from '@/views/ProductDetail.vue'
import Login from '@/views/Login.vue'
import Checkout from '@/views/Checkout.vue'
import CheckoutResult from '@/views/CheckoutResult.vue'
import OrderHistory from '@/views/OrderHistory.vue'
import Profile from '@/views/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: ProductList },
    { path: '/:category', component: ProductList },
    { path: '/chattest', component: ChatTest },
    { path: '/products/:id', component: ProductDetail },
    { path: '/login', component: Login },
    { path: '/checkout', component: Checkout },
    { path: '/checkoutresult/:order', component: CheckoutResult },
    { path: '/orderhistory', component: OrderHistory },
    { path: '/profile', component: Profile },
  ],
})

export default router
