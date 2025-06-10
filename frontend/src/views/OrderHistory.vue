<template>
  <v-container style="max-width: 100vw">
    <h2>order history</h2>
    <br />
    <v-row v-for="order in order_list">
      <v-col>
        <v-card style="width: 50vw" variant="outlined" elevation="16" hover>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th>order no</th>
                  <th>total</th>
                  <th>date</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>#{{ String(order.id).padStart(6, '0') }}</td>
                  <td>{{ order.actual_price }}</td>
                  <td>{{ formatToTaiwanTime(order.created_at) }}</td>
                  <td>
                    <v-btn
                      :icon="show ? 'mdi-chevron-up' : 'mdi-chevron-down'"
                      @click="order.show = !order.show"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
          <v-expand-transition>
            <div v-show="order.show">
              <v-divider></v-divider>

              <v-card-text>
                <v-table>
                  <thead>
                    <tr>
                      <th>product name</th>
                      <th>quantity</th>
                      <th>price</th>
                      <th>subtotal</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in order.items">
                      <td>{{ item.product.name }}</td>
                      <td>{{ item.quantity }}</td>
                      <td class="text-end">{{ item.product.price }}</td>
                      <td class="text-end">{{ caculateCartItemSubtotal(item) }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card-text>
            </div>
          </v-expand-transition>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { orderStore } from '@/stores/order'
const order = orderStore()
const order_list = ref([])
const fetchOrders = async () => {
  console.log('fetchOrders')
  const res = await order.getOrderList()
  order_list.value = res.map((order) => ({
    ...order,
    show: false, // 加上這個欄位
  }))
  console.log(order_list.value)
}
const caculateCartItemSubtotal = (item) => {
  return parseInt(item.quantity * Number(item.product.price))
}
const formatToTaiwanTime = (utcString) => {
  const utcDate = new Date(utcString)

  // 轉換成 UTC+8
  const taiwanOffset = 8 * 60 // 台灣是 UTC+8
  const localDate = new Date(utcDate.getTime() + taiwanOffset * 60 * 1000)

  const year = localDate.getUTCFullYear()
  const month = String(localDate.getUTCMonth() + 1).padStart(2, '0')
  const day = String(localDate.getUTCDate()).padStart(2, '0')
  const hour = String(localDate.getUTCHours()).padStart(2, '0')
  const minute = String(localDate.getUTCMinutes()).padStart(2, '0')
  const second = String(localDate.getUTCSeconds()).padStart(2, '0')

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`
}
onMounted(fetchOrders)
</script>
