<template>
  <v-container style="max-width: 80vw; width: 70vw">
    <h3>product list</h3>
    <v-data-table-server
      :items="product_list"
      :headers="headers"
      :items-length="total"
      v-model:items-per-page="itemsPerPage"
      @update:options="loadItems"
    >
      <template v-slot:item.actions="{ item }">
        <div class="d-flex ga-2 justify-end">
          <v-icon
            color="medium-emphasis"
            icon="mdi-pencil"
            size="small"
            @click="edit(item.id)"
          ></v-icon>

          <!-- <v-icon
            color="medium-emphasis"
            icon="mdi-delete"
            size="small"
            @click="remove(item.id)"
          ></v-icon> -->
        </div>
      </template>
    </v-data-table-server>
  </v-container>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/api/api'

const product_list = ref([])
const page_amount = ref(0)
// const page = ref(1)
const itemsPerPage = ref(20)
const total = ref(0)
const ordering = ref('-created_at')

const headers = ref([
  { title: 'ID', key: 'id', align: 'end', sortable: true },
  { title: 'Category', key: 'category_name', align: 'end', sortable: false },
  { title: 'Name', key: 'name', align: 'end', sortable: false },

  { title: 'Inventory', key: 'inventory', align: 'end', sortable: false },
  { title: 'Sold Count', key: 'sold_count', align: 'end', sortable: false },
  { title: 'Discount Percent(%)', key: 'discount_percent', align: 'end', sortable: false },
  { title: 'Price', key: 'price', align: 'end', sortable: true },
  { title: 'Create At', key: 'created_at', align: 'end', sortable: true },
  { title: 'Actions', key: 'actions', align: 'end', sortable: false },
])
const loadItems = async ({ page, itemsPerPage, sortBy }) => {
  console.log(page, itemsPerPage, sortBy)
  const params = {}
  if (sortBy.length) {
    const sortKey = sortBy[0].key
    const sortOrder = sortBy[0].order
    console.log(sortKey, sortOrder, (sortOrder === 'desc' ? '-' : '') + sortKey)
    ordering.value = (sortOrder === 'desc' ? '-' : '') + sortKey
  }
  const res = await api.fetchProducts(page, params, ordering.value, itemsPerPage)
  product_list.value = res.data.results
  page_amount.value = res.data.total_pages
  total.value = res.data.count
}
</script>
