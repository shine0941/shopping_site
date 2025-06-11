<template>
  <v-container style="max-width: 100vw">
    <!-- <v-row> filter </v-row> -->
    <!-- <v-row>sort</v-row> -->
    <v-row>
      <v-col v-for="(product, i) in product_list" :cols="3">
        <v-card color="primary" style="height: 56vh" variant="outlined" elevation="16" hover>
          <div style="height: 30vh; background-color: white; align-content: center">
            <v-img :src="product.images[0].image"></v-img>
          </div>
          <v-card-title class="text-wrap" style="height: 14vh">{{ product.name }}</v-card-title>
          <v-card-text style="text-align: right">
            <template v-if="product.discount_percent != 100">
              <h3>
                <del>${{ product.price }}</del> ${{
                  parseInt(product.price * (product.discount_percent / 100))
                }}
              </h3>
            </template>
            <template v-else>
              <h3>${{ product.price }}</h3>
            </template>
          </v-card-text>
          <v-card-actions>
            <v-col>
              <ProductDetailDialog v-model:product_info="product_list[i]"></ProductDetailDialog>
            </v-col>
            <v-col>
              <v-btn variant="outlined" block @click="addToCart(product)">
                <v-icon>mdi-cart</v-icon>
              </v-btn>
            </v-col>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api/api'
import { cartStore } from '@/stores/cart'
import ProductDetailDialog from '@/components/ProductDetailDialog.vue'
const route = useRoute()
const product_list = ref([])
const cart = cartStore()

const fetchProducts = async () => {
  const params = {}
  if (route.params.category) {
    params['category'] = route.params.category
  }
  const res = await api.fetchProducts(1, params)
  product_list.value = res.data
}
const addToCart = async (product) => {
  cart.appendCartItems(product.id)
}

onMounted(fetchProducts)
watch(route, fetchProducts, { immediate: true, deep: true })
</script>
