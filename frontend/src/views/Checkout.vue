<template>
  <v-container style="max-width: 100vw">
    <v-row>
      <v-col> Checkout </v-col>
    </v-row>
    <template v-if="test_data.length > 0">
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
                  <tr v-for="item in test_data" :key="item.id">
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
                  <tr v-for="item in test_data" :key="item.id">
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
        <!-- <v-btn color="primary" :disabled="stepper != stepper_items.length">Checkout</v-btn> -->
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
const test_data = ref([
  {
    id: 11,
    product: {
      id: 5,
      name: 'KODAK 柯達PIXPRO FZ55 5倍光學變焦 數位相機 28mm廣角鏡頭 原廠公司貨',
      price: '5595.00',
      images: [
        {
          id: 5,
          image: 'http://192.168.1.100:8001/product_images/product_images/000001_1732845704.webp',
          order: 0,
        },
      ],
    },
    subtotal: 11190,
    quantity: 2,
    cart: 1,
  },
  {
    id: 12,
    product: {
      id: 4,
      name: 'SONY 索尼DSC-RX100M7G 數位相機 (公司貨)',
      price: '36460.00',
      images: [
        {
          id: 4,
          image: 'http://192.168.1.100:8001/product_images/product_images/000001_1746416275.webp',
          order: 0,
        },
      ],
    },
    subtotal: 36460,
    quantity: 1,
    cart: 1,
  },
])
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
  console.log(item.quantity, Number(item.product.price))
  return item.quantity * Number(item.product.price)
}
const caculateCartSubtotal = () => {
  let subtotal = 0
  for (const item of test_data.value) {
    console.log(item)
    subtotal += item.quantity * Number(item.product.price)
  }

  return subtotal
}
onMounted(showCartItems)
</script>
