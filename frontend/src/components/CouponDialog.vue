<template>
  <v-dialog width="70vw" min-height="70vh">
    <template v-slot:activator="{ props: activatorProps }">
      <v-tooltip text="Create" location="bottom">
        <template v-slot:activator="{ props }">
          <v-btn variant="outlined" v-bind="mergeProps(activatorProps, props)">
            <v-icon>mdi-plus</v-icon>Create
          </v-btn>
        </template>
      </v-tooltip>
    </template>
    <template v-slot:default="{ isActive }">
      <v-card>
        <v-card-title> Create Coupon </v-card-title>
        <v-form @submit.prevent="submit">
          <v-card-text>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="code"
                  label="Code"
                  clearable
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-radio-group v-model="discount_type" label="Discount Type" inline>
                  <v-radio
                    v-for="item in discount_types"
                    :label="item.name"
                    :value="item.type"
                  ></v-radio>
                </v-radio-group>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="discount_value"
                  label="Discount Value"
                  clearable
                  :rules="[rules.required]"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <!-- <v-date-picker></v-date-picker> -->
                <v-date-input
                  v-model="valid_from"
                  label="Valid From"
                  clearable
                  :rules="[rules.required]"
                ></v-date-input>
              </v-col>
              <v-col>
                <v-date-input
                  v-model="valid_to"
                  label="Valid To"
                  clearable
                  :rules="[rules.required]"
                ></v-date-input>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-text-field
                  v-model="minimum_order_amount"
                  label="minimum_order_amount"
                  clearable
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field v-model="usage_limit" label="usage_limit" clearable></v-text-field>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn
              text="Close"
              @click="isActive.value = false"
              prepend-icon="mdi-close"
              color="primary"
            ></v-btn>
            <v-spacer></v-spacer>
            <v-btn
              type="submit"
              color="primary"
              text="submit"
              prepend-icon="mdi-check"
              @click="isActive.value = false"
              :disabled="false"
            ></v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>
<script setup>
import { mergeProps, ref } from 'vue'
import api from '@/api/api'

const emit = defineEmits(['fetchCoupons'])

const code = ref('')
const discount_type = ref('fixed')
const discount_value = ref(0)
const valid_from = ref('')
const valid_to = ref('')
const minimum_order_amount = ref(0)
const usage_limit = ref(0)
const discount_types = ref([
  { name: 'fixed', type: 'fixed' },
  { name: 'percent', type: 'percent' },
])
const rules = {
  required: (value) => !!value || 'Required.',
}
const submit = async () => {
  try {
    const params = {
      code: code.value,
      discount_type: discount_type.value,
      discount_value: discount_value.value,
      valid_from: valid_from.value,
      valid_to: valid_to.value,
      minimum_order_amount: minimum_order_amount.value,
      usage_limit: usage_limit.value,
    }
    console.log(params)
    const res = await api.createCoupon(params)
    // router.push('/')
    emit('fetchCoupons')
  } catch (err) {
    alert('登入失敗', err)
  }
}
</script>
