<template>
<div>
</div>
</template>

<script>
const d3 = require('d3')
export default {
  name: 'd3ColorMap',
  data: function() {
    return {
      colors: [],
    }
  },
  mounted: function() {
    let that = this
    this.colors.push(d3.rgb(255, 215, 0)) // gold
    this.colors.push(d3.rgb(50, 205, 50)) // lime green
    this.colors.push(d3.rgb(123, 104, 238)) // memdiumslateblue
    this.colors.push(d3.rgb(139, 69, 19)) // blown
    this.colors.push(d3.rgb(220, 20, 60)) // orange
    this.colors.push(d3.rgb(0, 100, 0)) // darkgreen
    this.colors.push(d3.rgb(0, 0, 205)) // mediumblue
    this.colors.push(d3.rgb(221, 160, 221)) // plum
    this.colors.push(d3.rgb(184, 134, 11)) // darkgoldenrod
    this.colors.push(d3.rgb(240, 230, 140)) // khaki
    this.colors.push(d3.rgb(199, 21, 133)) // mediumvioletred

  },
  methods: {
    send: function() {
      console.log('send')
    },
  }
}
</script>

<style>
</style>
