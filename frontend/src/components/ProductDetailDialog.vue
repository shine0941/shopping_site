<template>
  <v-dialog width="50vw" min-height="50vh">
    <template v-slot:activator="{ props: activatorProps }">
      <v-tooltip text="Detail" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn block variant="outlined" v-bind="mergeProps(activatorProps, props)">
            <v-icon>mdi-magnify-plus-outline</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card>
        <br />
        <v-row>
          <v-col>
            <div style="height: 30vh">
              <v-img :src="getProductImage()"></v-img>
            </div>
          </v-col>
          <v-col>
            <v-list>
              <v-list-item>
                <h3>{{ product_info.name }}</h3>
              </v-list-item>
              <v-divider :thickness="3" inset length="70%"></v-divider>
              <v-list-item>價格 {{ product_info.price }} 元</v-list-item>
              <v-divider :thickness="3" inset length="70%"></v-divider>
              <v-list-item>
                <v-select
                  v-model="amount"
                  label="數量"
                  :items="
                    Array.from({ length: Math.min(product_info.inventory, 10) }, (_, i) => i + 1)
                  "
                ></v-select>
              </v-list-item>
              <v-list-item>
                <v-btn
                  block
                  variant="outlined"
                  @click="addToCart(product_info)"
                  prepend-icon="mdi-cart"
                  >cart</v-btn
                >
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
        <v-row style="justify-content: right">
          <v-col style="max-width: 95%">
            <v-card-text v-html="product_info.description.replace(/\r\n/g, '<br />')">
            </v-card-text>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn text="Close" @click="isActive.value = false" prepend-icon="mdi-close"></v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
    </template>
  </v-dialog>
</template>
<script setup>
import { mergeProps, ref } from 'vue'
const props = defineProps({
  product_info: Object,
})
const amount = ref(1)
const getProductImage = () => {
  console.log('props.product_info', props.product_info)
  if (props.product_info && props.product_info.images) {
    return props.product_info.images[0].image
  }
  return ''
}
const addToCart = (product) => {
  cart.appendCartItems(product.id)
}
</script>
