<template>
  <v-container style="max-width: 100vw">
    <v-row>
      <v-col>
        <v-card style="width: 50vw">
          <v-card-title style="text-align: center">謝謝您的訂購</v-card-title>
          <v-card-subtitle style="text-align: center">
            訂單編號:#{{ order_data.id }} 已成立
          </v-card-subtitle>
          <v-card-text style="text-align: center">
            <v-table>
              <tbody>
                <tr v-for="item in order_data.items">
                  <td>
                    <v-img :src="item.product.images[0].image" style="width: 50px"></v-img>
                  </td>
                  <td>{{ item.product.name }}</td>
                  <td>{{ item.quantity }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { orderStore } from '@/stores/order'

const route = useRoute()
const order = orderStore()

const order_data = ref({})

const fetchOrder = async () => {
  console.log('fetchOrders')
  order_data.value = await order.getOrder(route.params.order)
}
onMounted(fetchOrder)
</script>
