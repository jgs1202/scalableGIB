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
    this.colors.push(d3.rgb(152, 251, 152)) // palegreen
    this.colors.push(d3.rgb(123, 104, 238)) // memdiumslateblue
    this.colors.push(d3.rgb(139, 69, 19)) // blown
    this.colors.push(d3.rgb(220, 20, 60)) // orange
    this.colors.push(d3.rgb(34, 139, 34)) // forestgreen
    this.colors.push(d3.rgb(0, 0, 128)) // navy
    this.colors.push(d3.rgb(221, 160, 221)) // plum
    this.colors.push(d3.rgb(184, 134, 11)) // darkgoldenrod
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
