<template>
  <v-container style="max-width: 80vw; width: 70vw">
    <h3>sales report</h3>
    <v-divider></v-divider>
    <v-card>
      <Bar :data="barData" :options="options" />
    </v-card>
    <!-- todo sales ranking -->
    <!-- todo sales ratio -->
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import { Bar } from 'vue-chartjs'
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)
const options = ref({
  responsive: true,
  maintainAspectRatio: false,
})
// const data = {
//   labels: [
//     'January',
//     'February',
//     'March',
//     'April',
//     'May',
//     'June',
//     'July',
//     'August',
//     'September',
//     'October',
//     'November',
//     'December',
//   ],
//   datasets: [
//     {
//       label: 'Data One',
//       backgroundColor: '#f87979',
//       data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
//     },
//   ],
// }
const barData = ref({ labels: [], datasets: [{ label: '', backgroundColor: '#f87979', data: [] }] })
const parseToBarData = (source_datas) => {
  const labels = []
  const datas = []
  const label = source_datas.year + '-' + source_datas.month
  for (const dat of source_datas.daily_sales) {
    labels.push(dat.day)
    datas.push(dat.sales)
  }
  barData.value = {
    labels: labels,
    datasets: [
      {
        label: label,
        backgroundColor: '#f87979',
        data: datas,
      },
    ],
  }
}
const init = async () => {
  //   const res = await api.getMonthlySales()
  //   console.log(res)

  const res2 = await api.getDailySales()
  parseToBarData(res2.data)
}
onMounted(init)
</script>
