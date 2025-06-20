import axios from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  baseURL: 'http://192.168.1.100:8001/',
  headers: {
    'Content-Type': 'application/json',
  },
})

function authHeader() {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.log('apiClient error', error)
    const userStore = useUserStore()
    if (error.response && error.response.status === 401) {
      userStore.logout()
      if (router.currentRoute.value.fullPath.includes('admin')) {
        router.push('/admin/login')
      } else {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  },
)

export default {
  fetchProducts(page = 1, params = {}, ordering = '-created_at', page_size = 20) {
    console.log('getProducts params', params)
    // return apiClient.get(`products/?page=${page}`, { params: params })

    return apiClient.get(
      `products/products/?page=${page}&ordering=${ordering}&page_size=${page_size}`,
      { params: params },
    )
  },
  fetchProduct(id) {
    return apiClient.get(`products/products/${id}/`)
  },
  login(params) {
    console.log('login', params)
    return apiClient.post(`/users/customer/login/`, params)
  },
  admin_login(params) {
    console.log('login', params)
    return apiClient.post(`/users/admin/login/`, params)
  },
  register(params) {
    return apiClient.post(`/users/customer/register/`, params)
  },
  updateUser(id, params) {
    console.log('params', params)
    return apiClient.patch(`/users/customers/${id}/`, params, { headers: authHeader() })
  },
  fetchUser(id) {
    return apiClient.get(`/users/customers/${id}/`, { headers: authHeader() })
  },
  refresh(params) {
    // console.log('login', params)
    return apiClient.post(`/api/token/refresh/`, params)
  },
  fetchCart() {
    return apiClient.get(`cart/carts/`, { headers: authHeader() })
  },
  fetchCartItems() {
    return apiClient.get(`cart/cart-items/`, { headers: authHeader() })
  },
  addToCart(params = {}) {
    console.log('params', params)
    return apiClient.post(`cart/cart-items/`, params, { headers: authHeader() })
  },
  updateCartItem(id, params) {
    console.log(id, 'params', params)
    return apiClient.patch(`cart/cart-items/${id}/`, params, { headers: authHeader() })
  },
  removeCartItem(id) {
    return apiClient.delete(`cart/cart-items/${id}/`, { headers: authHeader() })
  },
  createOrder(params = {}) {
    return apiClient.post(`orders/create/`, params, { headers: authHeader() })
  },
  fetchOrders() {
    console.log('api fetchOrders')
    return apiClient.get(`orders/orders/`, { headers: authHeader() })
  },
  fetchOrder(id) {
    console.log('api fetchOrder', id)
    return apiClient.get(`orders/orders/${id}/`, { headers: authHeader() })
  },
  fetchBackendOrders(page = 1, params = {}, ordering = '-created_at', page_size = 20) {
    console.log('api fetchBackendOrders')
    return apiClient.get(
      `orders/backend-list/?page=${page}&ordering=${ordering}&page_size=${page_size}`,
      { headers: authHeader() },
    )
  },

  fetchProductCategories() {
    return apiClient.get(`products/categories/`)
  },
  getMonthlySales() {
    return apiClient.get(`orders/stats/monthly-sales/`, { headers: authHeader() })
  },
  getDailySales() {
    return apiClient.get(`orders/stats/daily-sales/`, { headers: authHeader() })
  },
}
