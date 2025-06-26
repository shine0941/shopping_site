<template>
  <v-layout
    class="overflow-visible"
    style="height: 56px; position: fixed; width: 100vw; bottom: 0px"
  >
    <v-bottom-navigation grow>
      <v-btn value="recent" to="/videos/">
        <v-icon>mdi-video</v-icon>

        <span>CATEGORY</span>
      </v-btn>
      <v-btn value="recent" to="/comics/">
        <v-icon>mdi-cart</v-icon>

        <span>CART</span>
      </v-btn>
      <v-btn value="recent" to="/orderhistory/">
        <v-icon>mdi-history</v-icon>

        <span>ORDERS</span>
      </v-btn>
      <v-btn value="recent" to="/profile/">
        <v-icon>mdi-account</v-icon>

        <span>MEMBER</span>
      </v-btn>
    </v-bottom-navigation>
  </v-layout>
</template>
<script setup></script>
