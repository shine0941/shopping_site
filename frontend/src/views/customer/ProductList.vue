<template>
  <v-container style="max-width: 100vw">
    <!-- v-if="$deviceType == 'desktop'" -->
    <!-- <v-row> filter </v-row> -->
    <v-row>
      <v-col>
        <SortMenu @changeOrdering="changeOrdering"></SortMenu>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-pagination v-model:model-value="page" :length="page_amount"></v-pagination>
      </v-col>
    </v-row>
    <v-row>
      <v-col v-for="(product, i) in product_list" :cols="3">
        <v-card color="primary" style="height: 56vh" variant="outlined" elevation="16" hover>
          <div style="height: 30vh; background-color: white; align-content: center">
            <v-img :src="product.images[0].image">
              <ProductLabel v-model:product_info="product_list[i]"></ProductLabel>
            </v-img>
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
    <v-row>
      <v-col>
        <v-pagination v-model:model-value="page" :length="page_amount"></v-pagination>
      </v-col>
    </v-row>

    <!-- <template v-else>
      <v-row>
        <v-col v-for="(product, i) in product_list" :cols="6">
          <v-card color="primary" style="height: 43vh" variant="outlined" elevation="16" hover>
            <div style="height: 20vh; background-color: white; align-content: center">
              <v-img :src="product.images[0].image">
                <ProductLabel v-model:product_info="product_list[i]"></ProductLabel>
              </v-img>
            </div>
            <v-card-title class="text-wrap" style="height: 10vh">{{ product.name }}</v-card-title>
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
    </template> -->
  </v-container>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api/api'
import { cartStore } from '@/stores/cart'
import ProductDetailDialog from '@/components/ProductDetailDialog.vue'
import ProductLabel from '@/components/ProductLabel.vue'
import SortMenu from '@/components/SortMenu.vue'
const route = useRoute()
const product_list = ref([])
const cart = cartStore()
const ordering = ref('-created_at')
const page_amount = ref(0)
const page = ref(1)

const fetchProducts = async () => {
  const params = {}
  if (route.params.category) {
    params['category'] = route.params.category
  }
  const res = await api.fetchProducts(page.value, params, ordering.value)
  product_list.value = res.data.results
  page_amount.value = res.data.total_pages
}
const addToCart = async (product) => {
  cart.appendCartItems(product.id)
}
const changeOrdering = (new_ordering) => {
  ordering.value = new_ordering
  console.log(ordering.value)
}
watch(
  route,
  () => {
    console.log('target', 'route')
    page.value = 1
    fetchProducts()
  },
  { immediate: true, deep: true },
)
watch(ordering, () => {
  console.log('target', 'ordering')
  page.value = 1
  fetchProducts()
})
watch(page, () => {
  console.log('target', 'page')
  fetchProducts()
})
</script>
