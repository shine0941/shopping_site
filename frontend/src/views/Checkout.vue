<template>
  <v-container style="max-width: 100vw">
    <template v-if="cart.cartItems.length > 0">
      <v-stepper v-model="stepper" :items="stepper_items" style="width: 50vw" alt-labels>
        <template v-slot:item.1>
          <v-card title="Cart Items" flat>
            <v-sheet>
              <v-table>
                <thead>
                  <tr>
                    <th>pic</th>
                    <th>name</th>
                    <th>quantity</th>
                    <th>price</th>
                    <th>totalPrice</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in cart.cartItems" :key="item.id">
                    <td>
                      <v-img :src="item.product.images[0].image" style="width: 50px"></v-img>
                    </td>
                    <td>{{ item.product.name }}</td>
                    <td>
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
                    </td>
                    <td class="text-end">{{ item.product.price }}</td>
                    <td class="text-end">{{ caculateCartItemSubtotal(item) }}</td>
                  </tr>
                </tbody>
                <thead>
                  <tr>
                    <th>Total</th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th class="text-end">{{ caculateCartSubtotal() }}</th>
                  </tr>
                </thead>
              </v-table>
            </v-sheet>
          </v-card>
        </template>
        <template v-slot:item.2 :error="true">
          <v-card title="Shipping" flat>
            <v-radio-group v-model="shipping" label="Delivery Method">
              <v-radio
                v-for="item in shipping_data"
                :label="item.name"
                :value="item.price"
              ></v-radio>
            </v-radio-group>
          </v-card>
        </template>

        <template v-slot:item.3>
          <v-card title="Confirm" flat>
            <v-sheet>
              <v-table>
                <thead>
                  <tr>
                    <th>pic</th>
                    <th>name</th>
                    <th>quantity</th>
                    <th>price</th>
                    <th>totalPrice</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in cart.cartItems" :key="item.id">
                    <td>
                      <v-img :src="item.product.images[0].image" style="width: 50px"></v-img>
                    </td>
                    <td>{{ item.product.name }}</td>
                    <td>{{ item.quantity }}</td>
                    <td class="text-end">{{ item.product.price }}</td>
                    <td class="text-end">{{ caculateCartItemSubtotal(item) }}</td>
                  </tr>
                </tbody>
                <thead>
                  <tr>
                    <td>Shipping</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-end" v-text="shipping"></td>
                  </tr>
                  <tr>
                    <th>Total</th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th class="text-end">{{ caculateCartSubtotal() }}</th>
                  </tr>
                </thead>
              </v-table>
            </v-sheet>
          </v-card>
        </template>
      </v-stepper>
    </template>
    <br />
    <v-row>
      <v-col class="text-end">
        <v-btn color="primary" :disabled="stepper != stepper_items.length" @click="checkout"
          >Checkout</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { cartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
// const user = useUserStore()
const cart = cartStore()
const shipping = ref(0)
const shipping_data = ref([
  { name: 'Standard Shipping', price: 60 },
  { name: 'Priority Shipping', price: 100 },
  { name: 'Express Shipping', price: 200 },
])
const stepper = ref(null)
const stepper_items = ref(['Step 1', 'Step 2', 'Step 3'])
const showCartItems = () => {
  console.log(JSON.stringify(cart.cartItems))
}
const caculateCartItemSubtotal = (item) => {
  return item.quantity * Number(item.product.price)
}
const caculateCartSubtotal = () => {
  let subtotal = 0
  for (const item of cart.cartItems) {
    subtotal += item.quantity * Number(item.product.price)
  }

  return subtotal
}
const handleItemChange = async (item) => {
  console.log('handleItemChange', item)
  await cart.updateCartItem(item)
}
const checkout = () => {}
onMounted(showCartItems)
</script>
