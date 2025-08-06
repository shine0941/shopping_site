<template>
  <v-container style="max-width: 80vw; width: 70vw">
    <h3>coupon manage</h3>
    <br />
    <v-row>
      <v-col>
        <CouponDialog @fetchCoupons="loadItems"></CouponDialog>
      </v-col>
    </v-row>
    <v-data-table-server
      :items="coupon_list"
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
import CouponDialog from '@/components/CouponDialog.vue'

const coupon_list = ref([])
const page_amount = ref(0)
// const page = ref(1)
const itemsPerPage = ref(20)
const total = ref(0)
const ordering = ref('-created_at')
const headers = ref([
  { title: 'ID', key: 'id', align: 'end', sortable: true },
  { title: 'code', key: 'code', align: 'end', sortable: true },
  { title: 'discount type', key: 'discount_type', align: 'end', sortable: true },
  { title: 'discount value', key: 'discount_value', align: 'end', sortable: true },
  { title: 'valid from', key: 'valid_from', align: 'end', sortable: true },
  { title: 'valid to', key: 'valid_to', align: 'end', sortable: true },
  { title: 'minimum order amount', key: 'minimum_order_amount', align: 'end', sortable: true },
  { title: 'usage limit', key: 'usage_limit', align: 'end', sortable: true },
])

const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  console.log(page, itemsPerPage, sortBy)
  const params = {}
  //   if (sortBy.length) {
  //     const sortKey = sortBy[0].key
  //     const sortOrder = sortBy[0].order
  //     console.log(sortKey, sortOrder, (sortOrder === 'desc' ? '-' : '') + sortKey)
  //     ordering.value = (sortOrder === 'desc' ? '-' : '') + sortKey
  //   }
  const res = await api.fetchCoupons(page, params, ordering.value, itemsPerPage)
  coupon_list.value = res.data.results
  page_amount.value = res.data.total_pages
  total.value = res.data.count
}
</script>
