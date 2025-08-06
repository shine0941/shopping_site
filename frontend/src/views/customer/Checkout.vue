<template>
  <v-container style="max-width: 100vw">
    <template v-if="cart.cartItems.length > 0">
      <v-stepper
        v-model="stepper"
        :items="stepper_items"
        style="width: 50vw"
        alt-labels
        hide-actions
      >
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
                    <td style="width: 50%">{{ item.product.name }}</td>
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
                    <td class="text-end">
                      {{ parseInt(item.product.price * (item.product.discount_percent / 100)) }}
                    </td>
                    <td class="text-end">{{ caculateCartItemSubtotal(item) }}</td>
                  </tr>
                </tbody>
                <thead>
                  <tr>
                    <th>Total</th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th class="text-end">{{ caculateCartSubtotal(true) }}</th>
                  </tr>
                </thead>
              </v-table>
            </v-sheet>
          </v-card>
          <v-stepper-actions>
            <template v-slot:prev>
              <v-btn>Prev</v-btn>
            </template>
            <v-spacer></v-spacer>
            <template v-slot:next>
              <v-btn @click="stepper = 2">Next</v-btn>
            </template>
          </v-stepper-actions>
        </template>
        <template v-slot:item.2>
          <v-card title="Shipping info" flat>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="recipient"
                  label="Recipient"
                  clearable
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="address"
                  label="Address"
                  clearable
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="phone"
                  label="Phone"
                  clearable
                  :rules="[rules.required, rules.taiwanMobile]"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-card>
          <v-stepper-actions>
            <template v-slot:prev>
              <v-btn @click="stepper = 1">Prev</v-btn>
            </template>
            <v-spacer></v-spacer>
            <template v-slot:next>
              <v-btn @click="stepper = 3" :disabled="!shippingInfoValid">Next</v-btn>
            </template>
          </v-stepper-actions>
        </template>
        <template v-slot:item.3>
          <v-card title="Delivery Method & Coupon">
            <v-row>
              <v-col>
                <v-radio-group v-model="shipping_fee" label="Delivery Method">
                  <v-radio
                    v-for="item in shipping_data"
                    :label="item.name"
                    :value="item.price"
                  ></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
            <v-row>
              <v-col :cols="10">
                <v-text-field
                  v-model="coupon_code"
                  label="Coupon"
                  @update="checkCoupon"
                  clearable
                  :append-icon="coupon_code_icon"
                  :icon-color="coupon_code_icon_color"
                  :error="coupon_code_error"
                  :error-messages="coupon_code_error_msg"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-btn color="primary" @click="checkCoupon" :disabled="coupon_code.length == 0"
                  >Apply</v-btn
                >
              </v-col>
            </v-row>
          </v-card>
          <v-stepper-actions>
            <template v-slot:prev>
              <v-btn @click="stepper = 2">Prev</v-btn>
            </template>
            <v-spacer></v-spacer>
            <template v-slot:next>
              <v-btn @click="stepper = 4">Next</v-btn>
            </template>
          </v-stepper-actions>
        </template>
        <template v-slot:item.4>
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
                    <td class="text-end">
                      {{ parseInt(item.product.price * (item.product.discount_percent / 100)) }}
                    </td>
                    <td class="text-end">{{ caculateCartItemSubtotal(item) }}</td>
                  </tr>
                </tbody>
                <thead>
                  <tr>
                    <td>Shipping</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-end" v-text="shipping_fee"></td>
                  </tr>
                  <tr v-if="coupon">
                    <td>Coupon</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-end" v-text="coupon.discount_value"></td>
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
          <v-stepper-actions>
            <template v-slot:prev>
              <v-btn @click="stepper = 3">Prev</v-btn>
            </template>
            <v-spacer></v-spacer>
            <template v-slot:next>
              <v-btn>Next</v-btn>
            </template>
          </v-stepper-actions>
        </template>
      </v-stepper>
    </template>
    <br />
    <v-row>
      <v-col class="text-end">
        <v-btn
          color="primary"
          :disabled="stepper != stepper_items.length"
          @click="checkout"
          :loading="loading"
          >Checkout</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { cartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import api from '@/api/api'
// const user = useUserStore()
const cart = cartStore()
const router = useRouter()
const shipping_fee = ref(60)
const shipping_data = ref([
  { name: 'Standard Shipping(+60)', price: 60 },
  { name: 'Priority Shipping(+100)', price: 100 },
  { name: 'Express Shipping(+200)', price: 200 },
])
const stepper = ref(null)
const stepper_items = ref(['Step 1', 'Step 2', 'Step 3', 'Step 4'])
const loading = ref(false)

const recipient = ref('王小明')
const address = ref('112台北市北投區石牌路一段39巷100號')
const phone = ref('0987654321')
const coupon_code = ref('')
const coupon = ref(null)
const coupon_code_icon = ref('')
const coupon_code_icon_color = ref('')
const coupon_code_error = ref(false)
const coupon_code_error_msg = ref('')

const caculateCartItemSubtotal = (item) => {
  return parseInt(
    item.quantity * parseInt(item.product.price * (item.product.discount_percent / 100)),
  )
}
const caculateCartSubtotal = (item_only = false) => {
  let subtotal = 0
  for (const item of cart.cartItems) {
    subtotal += item.quantity * parseInt(item.product.price * (item.product.discount_percent / 100))
  }
  if (!item_only) {
    subtotal += parseInt(shipping_fee.value)
    if (coupon.value) {
      subtotal -= parseInt(coupon.value.discount_value)
    }
  }

  return parseInt(subtotal)
}
const handleItemChange = async (item) => {
  console.log('handleItemChange', item)
  await cart.updateCartItem(item)
}
const checkout = async () => {
  loading.value = true
  console.log('checkout')
  const params = {
    shipping_fee: shipping_fee.value,
    coupon_code: coupon_code.value,
    recipient: recipient.value,
    address: address.value,
    phone: phone.value,
  }
  const res = await cart.checkout(params)
  console.log('res', res)
  if (res.status == 201) {
    loading.value = false
    const order = res.data.id
    router.push(`/checkoutresult/${order}`)
  } else {
  }
}
const rules = {
  required: (value) => !!value || 'Required.',
  taiwanMobile: (value) => /^09\d{8}$/.test(value) || 'Please enter a valid Taiwan mobile number',
}
const shippingInfoValid = computed(() => {
  return (
    rules.required(recipient.value) === true &&
    rules.required(address.value) === true &&
    rules.required(phone.value) === true &&
    rules.taiwanMobile(phone.value)
  )
})
const checkCoupon = async () => {
  if (coupon_code.value) {
    const params = { coupon_code: coupon_code.value }
    const res = await api.checkCoupon(params)
    if (res.data.is_valid) {
      coupon.value = res.data.coupon_data
      coupon_code_error.value = false
      coupon_code_error_msg.value = ''
      coupon_code_icon.value = 'mdi-check'
      coupon_code_icon_color.value = 'green'
    } else {
      coupon.value = null
      coupon_code_error.value = true
      coupon_code_error_msg.value = 'invalid coupon code'
      coupon_code_icon.value = 'mdi-close'
      coupon_code_icon_color.value = 'red'
    }

    console.log(coupon.value)
  } else {
    coupon.value = null
    coupon_code_error.value = false
    coupon_code_error_msg.value = ''
    coupon_code_icon.value = ''
    coupon_code_icon_color.value = 'green'
  }
}
</script>
