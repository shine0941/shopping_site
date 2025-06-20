<template>
  <v-container style="max-width: 100vw; width: 80vw">
    <v-row v-if="product_info">
      <v-col>
        <div style="height: 30vh">
          <v-img :src="getProductImage()"></v-img>
        </div>
      </v-col>
      <v-col>
        <v-list>
          <v-list-item>{{ product_info.name }}</v-list-item>
          <v-divider :thickness="3" inset length="70%"></v-divider>
          <v-list-item>價格{{ product_info.price }}元</v-list-item>
          <v-divider :thickness="3" inset length="70%"></v-divider>
          <v-list-item>
            <v-select
              v-model="amount"
              label="數量"
              :items="Array.from({ length: Math.min(product_info.inventory, 10) }, (_, i) => i + 1)"
            ></v-select>
          </v-list-item>
          <v-list-item>
            <v-btn @click="addToCart">cart</v-btn>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <!-- <v-col>detail</v-col> -->
    </v-row>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/api'
const route = useRoute()
const product_info = ref({})
const amount = ref(1)

const fetchProduct = async () => {
  const id = route.params.id
  const res = await api.fetchProduct(id)
  product_info.value = res.data
}
const getProductImage = () => {
  if (product_info && product_info.value.images) {
    return product_info.value.images[0].image
  }
  return ''
}
const addToCart = () => {
  console.log(amount)
}
onMounted(fetchProduct)
</script>
