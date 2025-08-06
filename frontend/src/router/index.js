import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // pinia or other store
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/FrontLayout.vue'),
      children: [
        { path: '', component: () => import('@/views/customer/ProductList.vue') },
        { path: ':category', component: () => import('@/views/customer/ProductList.vue') },
        // { path: 'chattest', component: () => import('@/views/customer/ChatTest.vue') },
        { path: 'products/:id', component: () => import('@/views/customer/ProductDetail.vue') },
        {
          path: 'login',
          name: 'customer-login',
          component: () => import('@/views/customer/Login.vue'),
        },
        {
          path: 'checkout',
          component: () => import('@/views/customer/Checkout.vue'),
          meta: { requiresAuth: true, redirect: 'login' },
        },
        {
          path: 'checkoutresult/:order',
          component: () => import('@/views/customer/CheckoutResult.vue'),
          meta: { requiresAuth: true, redirect: 'login' },
        },
        {
          path: 'orderhistory',
          component: () => import('@/views/customer/OrderHistory.vue'),
          meta: { requiresAuth: true, redirect: 'login' },
        },
        {
          path: 'profile',
          component: () => import('@/views/customer/Profile.vue'),
          meta: { requiresAuth: true, redirect: 'login' },
        },
      ],
    },
    {
      path: '/admin',
      component: () => import('@/layouts/AdminLayout.vue'),
      // meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'AdminDashboard',
          component: () => import('@/views/admin/Index.vue'),
          // meta: { requiresAuth: true, requiresAdmin: true },
        },
        { path: 'login', name: 'admin-login', component: () => import('@/views/admin/Login.vue') },
        {
          path: 'products',
          name: 'product-list',
          component: () => import('@/views/admin/ProductList.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'orders',
          name: 'order-list',
          component: () => import('@/views/admin/OrderList.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'sales',
          name: 'sales-report',
          component: () => import('@/views/admin/SalesReport.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'coupons',
          name: 'coupon-manage',
          component: () => import('@/views/admin/CouponManage.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
        },
        {
          path: 'chats',
          name: 'customer-service',
          component: () => import('@/views/admin/CustomerService.vue'),
          meta: { requiresAuth: true, requiresAdmin: true },
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const user = useUserStore()
  const auth = useAuthStore()
  user.init()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    // 沒登入轉跳
    if (to.meta.requiresAdmin) {
      return next({ name: 'admin-login' })
    }
    return next({ name: 'customer-login' })
  }

  // if (to.meta.requiresAdmin && !auth.isAdmin) {
  //   // 不是 admin 轉跳首頁
  //   return next({ name: 'Home' })
  // }

  if (to.meta.role && auth.user.role !== to.meta.role) {
    return next({ name: 'Home' }) // 無權限，導回首頁
  }

  next()
})

export default router
