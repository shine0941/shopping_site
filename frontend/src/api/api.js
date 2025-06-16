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
      router.push('/login')
    }
    return Promise.reject(error)
  },
)

export default {
  fetchProducts(page = 1, params = {}) {
    console.log('getProducts params', params)
    // return apiClient.get(`products/?page=${page}`, { params: params })
    return apiClient.get(`products/products/`, { params: params })
  },
  fetchProduct(id) {
    return apiClient.get(`products/products/${id}/`)
  },
  login(params) {
    console.log('login', params)
    return apiClient.post(`/users/customer/login/`, params)
  },
  register(params) {
    return apiClient.post(`/users/customer/register/`, params)
  },
  updateUser(id, params) {
    console.log('params', params)
    return apiClient.patch(`/users/customers/${id}/`, params, { headers: authHeader() })
  },
  refresh(params) {
    console.log('login', params)
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
  fetchProductCategories() {
    return apiClient.get(`products/categories/`)
  },
  //   getCategorys() {
  //     return apiClient.get(`categorys/`)
  //   },
  //   getTagCategorys() {
  //     return apiClient.get(`tagcategorys/`)
  //   },
  //   getTags() {
  //     return apiClient.get(`tags/`)
  //   },
  //   getActors() {
  //     return apiClient.get(`actors/`)
  //   },
  //   createActor(data) {
  //     console.log('createActor', data)
  //     return apiClient.post(`actors/`, data)
  //   },
  //   updateVideo(id, data) {
  //     // return apiClient.put(`videos/${id}/`, data)
  //     return apiClient.patch(`videos/${id}/`, data)
  //   },
  //   createVideoClip(id, data) {
  //     return apiClient.post(`videos/${id}/add_clip/`, data)
  //   },
  //   getRandomVideo(params) {
  //     return apiClient.get(`videos/random/`, { params: params })
  //   },
}
