<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App from './components/App.vue'
import tutorial from './components/tutorial.vue'
import Menu from './components/menu.vue'
import dataInput from './components/dataInput.vue'
import histgram from './components/histgram.vue'
import scarf from './components/scarf.vue'
Vue.component('dataInput', dataInput)
Vue.component('tutorial', tutorial)
Vue.component('App', App)
Vue.component('Menu', Menu)
Vue.component('histgram', histgram)
Vue.component('scarf', scarf)
export default {
  name: 'home',
  data: function() {
    return {
      currentPage: null,
      userName: 'null',
      gender: 'null',
      age: null,
      already: 0,
      total: 10,
      nums: [0, 0],
      total: 120,
      levelIndex: ['high', 'low'],
      level: 0,
    }
  },
  mounted: function(){
    console.log('home mounted')
    this.currentPage = 'dataInput'
  }
}
</script>
