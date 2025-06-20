<template>
  <v-container style="max-width: 80vw; width: 70vw">
    <h3>order list</h3>
    <v-data-table-server
      :items="order_list"
      :headers="headers"
      :items-length="total"
      v-model:items-per-page="itemsPerPage"
      @update:options="loadItems"
    ></v-data-table-server>
  </v-container>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/api/api'

const order_list = ref([])
const page_amount = ref(0)
// const page = ref(1)
const itemsPerPage = ref(20)
const total = ref(0)
const ordering = ref('-created_at')

const headers = ref([
  { title: 'ID', key: 'id', align: 'end', sortable: true },
  { title: 'customer', key: 'customer', align: 'end', sortable: true },
  { title: 'created_at', key: 'created_at', align: 'end', sortable: true },
  { title: 'total_price', key: 'total_price', align: 'end', sortable: true },
  { title: 'shipping_fee', key: 'shipping_fee', align: 'end', sortable: true },
  { title: 'actual_price', key: 'actual_price', align: 'end', sortable: true },
  { title: 'order_status', key: 'order_status', align: 'end', sortable: true },
])

const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  const params = {}
  const res = await api.fetchBackendOrders(page, params, ordering.value)
  order_list.value = res.data.results
  page_amount.value = res.data.total_pages
  total.value = res.data.count
}
</script>
