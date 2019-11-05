<template>
<div id="app">
  <input id="checkGroupInABox" type="checkbox">Group in a Box</input>
  <input id="checkShowTreemap" type="checkbox">Show Template</input>
  <select id="selectTemplate" type="select">
      <option value="treemap">Treemap</option>
      <option value="force">Force</option>
    </select>
  <div id="chart"></div>
</div>
</template>

<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/queue-async/1.0.7/queue.min.js"></script> -->
<script>
const d3 = require('d3')
export default {
  name: 'app',
  data() {
    return {