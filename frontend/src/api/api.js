import axios from 'axios'

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
export default {
  fetchProducts(page = 1, params = {}) {
    console.log('getProducts params', params)
    // return apiClient.get(`products/?page=${page}`, { params: params })
    return apiClient.get(`products/products/`)
  },
  fetchProduct(id) {
    return apiClient.get(`products/products/${id}/`)
  },
  login(params) {
    console.log('login', params)
    return apiClient.post(`/users/customer/login/`, params)
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
