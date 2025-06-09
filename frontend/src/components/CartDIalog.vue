<template>
  <v-dialog max-width="500">
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn v-bind="activatorProps" icon="mdi-cart">
        <v-icon>mdi-cart</v-icon>
        <!-- <div style="position: absolute; top: 0; right: 0">
          {{ cart.cartItems.length }}
        </div> -->
        <div v-if="cart.cartItems.length > 0">
          {{ cart.cartItems.length }}
        </div>
      </v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card>
        <v-row>
          <v-col>
            <v-card-title> Cart </v-card-title>
          </v-col>
          <v-col style="text-align: right">
            <!-- <v-icon @click="isActive.value = false">mdi-close</v-icon> -->
          </v-col>
        </v-row>

        <v-card-text>
          <template v-if="cart.cartItems.length > 0">
            <v-list>
              <v-list-item v-for="item in cart.cartItems" :key="item.id">
                <template v-slot:prepend>
                  <v-img :src="item.product.images[0].image" style="width: 50px"></v-img>
                </template>
                <v-card>{{ item.product.name }}</v-card>
                <template v-slot:append>
                  <div>
                    <v-number-input
                      v-model="item.quantity"
                      :reverse="false"
                      controlVariant="split"
                      label=""
                      :hideInput="false"
                      inset
                      variant="solo-filled"
                      @update:model-value="handleItemChange(item)"
                    ></v-number-input>
                  </div>
                  <div>
                    <v-icon>mdi-close</v-icon>
                  </div>
                </template>

                <!-- {{ item.product.name }}{{ item.quantity }} -->
              </v-list-item>
            </v-list>
          </template>
          <template v-else>
            <div>empty</div>
          </template>
        </v-card-text>

        <v-card-actions>
          <v-btn text="Close Cart" @click="isActive.value = false"></v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text="Checkout"
            prepend-icon="mdi-cart"
            to="/checkout/"
            @click="isActive.value = false"
            :disabled="cart.cartItems.length == 0"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>
<script setup>
import { onMounted, watch } from 'vue'
import { cartStore } from '@/stores/cart'
// import { useUserStore } from '@/stores/user'
// const user = useUserStore()
const cart = cartStore()
const showCartItems = () => {
  console.log('cartItems', typeof cart.cartItems, cart.cartItems)
}
const handleItemChange = async (item) => {
  console.log(item)
  await cart.updateCartItem(item)
}
onMounted(showCartItems)
</script>
