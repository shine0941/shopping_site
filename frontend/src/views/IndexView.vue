<template>
  <v-container style="max-width: 100vw">
    <!-- <v-row> filter </v-row> -->
    <!-- <v-row>sort</v-row> -->
    <v-row>
      <v-col v-for="product in product_list" :cols="3">
        <v-card color="primary" style="height: 50vh" variant="outlined" elevation="16" hover>
          <div style="height: 30vh; background-color: white; align-content: center">
            <v-img :src="product.images[0].image"></v-img>
          </div>
          <v-card-title class="text-wrap" style="height: 14vh">{{ product.name }}</v-card-title>
          <!-- <v-card-subtitle></v-card-subtitle> -->
          <v-card-actions>
            <v-col>
              <v-btn block border @click="goDetail(product)">
                <v-icon>mdi-magnify-plus-outline</v-icon>
              </v-btn>
            </v-col>

            <v-col>
              <v-btn block border @click="addToCart(product)">
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api'
const router = useRouter()
const product_list = ref([])

const goDetail = (product) => {
  console.log('goDetail', product)
  router.push(`/products/${product.id}`)
}
const fetchProducts = async () => {
  const res = await api.fetchProducts()
  product_list.value = res.data
}
const addToCart = async (product) => {
  const params = {
    quantity: 1,
    product: product.id,
  }
  const res = await api.addToCart(params)
}

onMounted(fetchProducts)
</script>
