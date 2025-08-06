<template>
  <v-dialog width="40vw" min-height="30vh">
    <template v-slot:activator="{ props: activatorProps }">
      <v-tooltip text="Cart" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="mergeProps(activatorProps, props)" icon="mdi-cart">
            <v-icon>mdi-cart</v-icon>
            <div v-if="cart.cartItems.length > 0">
              {{ cart.cartItems.length }}
            </div>
          </v-btn>
        </template>
      </v-tooltip>
    </template>

    <template v-slot:default="{ isActive }">
      <v-card>
        <v-row>
          <v-col>
            <v-card-title> Cart </v-card-title>
          </v-col>
          <v-col style="text-align: right"> </v-col>
        </v-row>

        <v-card-text>
          <template v-if="cart.cartItems.length > 0">
            <v-list>
              <template v-for="(item, index) in cart.cartItems" :key="item.id">
                <v-list-item>
                  <template v-slot:prepend>
                    <v-img :src="item.product.images[0].image" style="width: 50px"></v-img>
                  </template>
                  <v-row>
                    <v-col :cols="8" style="align-content: center">
                      <div style="align-content: center; margin-left: 10px">
                        {{ item.product.name }}
                      </div>
                    </v-col>
                    <v-col md="4" sm="4">
                      <v-number-input
                        v-model="item.quantity"
                        :reverse="false"
                        controlVariant="split"
                        label=""
                        :hideInput="false"
                        inset
                        variant="solo-filled"
                        @update:model-value="handleItemChange(item)"
                        style="margin-right: 10px"
                      ></v-number-input>
                    </v-col>
                  </v-row>
                  <template v-slot:append>
                    <div style="align-content: center">
                      <v-icon @click="removeItem(item)">mdi-trash-can</v-icon>
                    </div>
                  </template>
                </v-list-item>
                <v-divider v-if="index + 1 < cart.cartItems.length"></v-divider>
              </template>
            </v-list>
          </template>
          <template v-else>
            <div>empty</div>
          </template>
        </v-card-text>

        <v-card-actions>
          <v-btn
            text="Close Cart"
            @click="isActive.value = false"
            prepend-icon="mdi-close"
            color="primary"
          ></v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
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
import { mergeProps } from 'vue'
import { cartStore } from '@/stores/cart'
const cart = cartStore()
const handleItemChange = async (item) => {
  await cart.updateCartItem(item)
}
const removeItem = async (item) => {
  await cart.removeCartItem(item)
}
</script>
