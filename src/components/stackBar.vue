<template>
  <div class='stackBar'>
    <barData></barData>
  </div>
</template>

<script>
import Vue from 'vue'
import barData from './barData.vue'
Vue.component('barData', barData)
export default {
  name: 'stackBar',
  data: function() {
    return {
      components: {
        barData,
      },
    }
  },
  methods: {
  },
}
</script>

<style>
.stackBar {
  width: 80%;
  height: 80%
}
</style>
