<template>
<div id="home">
  <component :is="currentPage"></component>
</div>
</template>

<script>
import Vue from 'vue'
import App from './components/App.vue'
import Menu from './components/menu.vue'
import dataInput from './components/dataInput.vue'
Vue.component('dataInput', dataInput)
Vue.component('App', App)
Vue.component('Menu', Menu)
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
      levelIndex: ['high', 'low'],
      level: null,
    }
  },
  mounted: function(){
    console.log('home mounted')
    this.currentPage = 'dataInput'
  }
}
</script>
