<template>
<div>
  <div><d3ColorMap ref='d3ColorMap'></d3ColorMap></div>
  <div id="app" class="app">
    <el-container style="width: 100%">
      <div class="svg-container" :style="{width: settings.width + '%'}">
        <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
          <g id="nodes">{{nodes}}</g>
          <g id="links">{{links}}</g>
          <g id='boxes'>{{boxes}}</g>
        </svg>
      </div>
    </el-container>
  </div>
  <div class="sync">
  </div>
</div>
</template>

<script>
import axios from 'axios'
import Vue from 'vue'
import d3ColorMap from './d3ColorMap.vue'
Vue.component('d3ColorMap', d3ColorMap)
const d3 = require('d3')
const swal = require('sweetalert')
export default {
  name: 'app',
  data: function() {
    return {
      graph: null,
      simulation: null,
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      nodeData: {
        name: null,
        group: null,
      },
      nodes: [],
      links: [],
      boxes: [],
      choice: [],
      dataMax: null,
      startTime: null,
      time: null,
      answer: null,
      totalQue: 50,
      level: null,
      file: null,
      normalSize: 2,
      relatedSize: 3,
      selectSize: 3,
      selectedNodes: [],
      nodeHistory: [],
      relatedNodes: [],
      twosideLinks: [],
      onesideLinks: [],
      twosideThickness: 3,
      onesideThickness: 1.5,
      colors: [],
      givenNodesColors: [d3.rgb(100, 149, 237), d3.rgb(64, 224, 208)],
      twosideColor: d3.rgb(255, 99, 71),
      onesideColor:  d3.rgb(100, 149, 237),
      answerColor: d3.rgb(255, 105, 180),
      linkOpacity: 0.6,
      jsonDataInfo: "sample",
      tableData: [],
      timer: null,
      limit_second: 30,
      givenNodesStrokeWidth: 2,
    }
  },
  mounted: function() {
    window.addEventListener('keyup', this.onClick)
    var that = this;
    that.dataMax = that.$parent.total / 6
    that.colors = that.$refs.d3ColorMap.colors
    console.log('mounted')
    that.restart(true)
  },
  methods: {
    restart: function(first) {
      var that = this;
      console.log('num is ' + '' + that.$parent.nums[that.$parent.level])
      if ((that.$parent.nums[that.$parent.level] % that.dataMax == 0) && (that.$parent.nums[that.$parent.level] != 0) && (!first)) {
        if (that.$parent.nums[that.$parent.level] == this.$parent.total) {
          this.$parent.already = 1
        }
        window.removeEventListener('keyup', that.onClick)
        this.$parent.currentPage = 'Menu'
      } else {
        // d3.json("./src/data/" + that.$parent.levelIndex[that.$parent.level] + '/' + that.$parent.nums[that.$parent.level] + ".json").then(function(graph) {
        d3.json("./src/data/random/" + that.$parent.nums[that.$parent.level] + ".json").then(function(graph) {
          that.graph = graph
          if (that.graph.groupSize == 10) {
            that.level = 0
          } else {
            that.level = 1
          }
          that.setTable()
          that.nodeHistory = []
          that.relatedNodes = []
          that.selectedNodes = []
          that.selectedNodes.push(that.graph.shortest_path.nodes[0])
          that.selectedNodes.push(that.graph.shortest_path.nodes[1])
          for (let i=0; i < that.graph.nodes.length; i++){
            that.relatedNodes.push([])
          }
          that.twosideLinks = []
          that.onesideLinks = []
          for (let i=0; i < that.graph.links.length; i++){
            that.twosideLinks.push([])
            that.onesideLinks.push([])
          }
          that.graph.groups.pop()
          that.$set(that.boxes, that.reBoxes())
          that.$set(that.links, that.reLinks())
          that.$set(that.nodes, that.reNodes())
          that.initialEdgeNodesHighliht()
        })
        let sync = document.getElementsByClassName('sync')
        for(let i=0; i<sync.length; i++){
          if ( that.$parent.nums[that.$parent.level] % 2 == 0 ){
            sync[i].style.background = 'black'
          } else {
            sync[i].style.background = 'white'
          }
        }
        that.startTime = Date.now()
        that.timer = setTimeout(that.timelimit, that.limit_second * 1000);
        that.$parent.nums[that.$parent.level] += 1
      }
    },
    setTable() {
      let that = this
      let _tableData = {}
      that.tableData = []
      _tableData.nodes = that.graph.nodes.length
      _tableData.links = that.graph.links.length
      _tableData.groups = that.graph.groups.length
      _tableData.density = Math.round(that.graph.density * 100000) / 100000
      _tableData.degree = Math.round(that.graph.averageDegree * 1000) / 1000
      _tableData.difficulty = Math.round(parseFloat(that.graph.shortest_path.difficulty) * 100 * 1000) / 1000
      that.tableData.push(_tableData)
    },
    reNodes: function() {
      var that = this;
      if (that.graph) {
        d3.selectAll('circle').remove()
        d3.select("svg").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.graph.nodes)
          .enter().append("circle")
          .attr('cx', that.settings.svgWigth / 2)
          .attr('cy', that.settings.svgHeight / 2)
          .attr('r', that.normalSize)
        return d3.selectAll("circle")
          .each(function(d, i) {
            let selection = d3.select(this)
            selection.transition()
              .attr('cx', that.graph.nodes[i].cx)
              .attr("cy", that.graph.nodes[i].cy)
              .attr("fill", function(d, i) {
                // return that.color(d.group / that.graph.groups.length);
                // return d3.interpolateRainbow(d.group / that.graph.groups.length)
                if (that.graph.shortest_path.nodes.indexOf(d.id) >= 0) {
                  return that.twosideColor
                } else {
                  return 'black'
                }
              })
              selection.on('mouseover', function(d, i){
                selection.attr('r', that.selectSize)
                let argvs = {}
                if (d.name) {
                  that.nodeData.name = d.name
                } if (d.group) {
                  that.nodeData.group = d.group
                }
              })
              selection.on('click', function(d, i){
                // console.log('click')
                that.selectNode(d, i)
              })
              selection.on('mouseout', function(d, i){
                that.nodeData.name = null
                that.nodeData.group = null
                if ((that.selectedNodes.indexOf(d.id) < 0) && (that.relatedNodes[d.id].length === 0)){
                  selection.attr('r', that.normalSize)
                } else if ((that.selectedNodes.indexOf(d.id) < 0) && (that.relatedNodes[d.id].length !== 0)){
                  selection.attr('r', that.relatedSize)
                }
              })
          })
      }
    },
    checkAnswer: function() {
      let that = this
      let answerPaths = that.graph.shortest_path.answers
      let flag = 0
      for (let path=0; path<that.graph.shortest_path.answers.length; ++path) {
        for (let node=0; node<that.selectedNodes.length; ++node) {
          if (that.graph.shortest_path.answers[path].indexOf(that.selectedNodes[node]) >= 0) {
            if (node == that.selectedNodes.length - 1) {
              if (node == that.graph.shortest_path.answers[path].length - 1)
              flag = 1
            }
          } else {
            break
          }
        }
      }
      return flag
    },
    enterAfterCorrect: function(event) {
      console.log('correct')
      console.log(event.keyCode)
      if (event.keyCode == 13) {
        let that = this
        window.removeEventListener('keyup', that.enterAfterCorrect)
        d3.selectAll('rect').attr('stroke-width', 0.6).attr('stroke', 'black')
        d3.selectAll('circle').remove()
        d3.selectAll('line').remove()
        d3.selectAll('rect').remove()
        window.addEventListener('keyup', that.onClick)
        that.restart(false)
      }
    },
    autoCorrect: function() {
      let that = this
      that.time = Date.now() - that.startTime
      window.removeEventListener('keyup', that.onClick)
      clearTimeout(that.timer)
      const params = new URLSearchParams()
      // username, gender, age, layout, path, groupSize, file, answer, time
      let now = new Date()
      let date = '' + now.getFullYear() + (now.getMonth() + 1) + now.getDate() + now.getHours() + now.getMinutes()
      params.set('date', date)
      params.set('userName', that.$parent.userName)
      params.set('gender', that.$parent.gender)
      params.set('age', that.$parent.age)
      params.set('layout', that.graph.layout)
      params.set('level', that.$parent.level)
      let nodeHistoryString = ""
        for (let i=0; i<that.nodeHistory.length; ++i){
          if (i != 0) {
            nodeHistoryString += " "
          }
          nodeHistoryString += "" + that.nodeHistory[i]
        }
        params.set('nodeHistory', nodeHistoryString)
      let pathString = ""
      for (let i=0; i<that.selectedNodes.length; ++i){
        if (i != 0) {
          pathString += " "
        }
        pathString += "" + that.selectedNodes[i]
      }
      params.set('path', pathString)
      params.set('path_length_difference', that.graph.shortest_path.length - that.selectedNodes.length)
      params.set('groupSize', that.graph.groupSize)
      params.set('origin_filename', '' + that.graph.file)
      params.set('filename', '' + that.graph.arranged_filename)
      that.answer = 1
      params.set('answer', that.answer)
      params.set('time', that.time)
      console.log(params)
      const url = `http://127.0.0.1:5000/data/${params.toString()}`
      axios.get(url)
        .then(res => {
          // console.log(res.data)
        })
      that.choice = []
      window.addEventListener('keyup', that.enterAfterCorrect)
    },
    timelimit: function() {
      var that = this
      clearTimeout(that.timer)
      that.time = Date.now() - that.startTime
      const params = new URLSearchParams()
      // username, gender, age, layout, path, groupSize, file, answer, time
      let now = new Date()
      let date = '' + now.getFullYear() + (now.getMonth() + 1) + now.getDate() + now.getHours() + now.getMinutes()
      params.set('date', date)
      params.set('userName', that.$parent.userName)
      params.set('gender', that.$parent.gender)
      params.set('age', that.$parent.age)
      params.set('layout', that.graph.layout)
      params.set('level', that.$parent.level)
      let nodeHistoryString = ""
        for (let i=0; i<that.nodeHistory.length; ++i){
          if (i != 0) {
            nodeHistoryString += " "
          }
          nodeHistoryString += "" + that.nodeHistory[i]
        }
        params.set('nodeHistory', nodeHistoryString)
      let pathString = ""
      for (let i=0; i<that.selectedNodes.length; ++i){
        if (i != 0) {
          pathString += " "
        }
        pathString += "" + that.selectedNodes[i]
      }
      params.set('path', pathString)
      params.set('path_length_difference', that.graph.shortest_path.length - that.selectedNodes.length)
      params.set('groupSize', that.graph.groupSize)
      params.set('origin_filename', '' + that.graph.file)
      params.set('filename', '' + that.graph.arranged_filename)
      if (that.checkAnswer() == 1){
        that.answer = 1
      } else {
        that.answer = 0
      }
      params.set('answer', that.answer)
      params.set('time', that.limit_second * 1000)
      console.log(params)
      const url = `http://127.0.0.1:5000/data/${params.toString()}`
      axios.get(url)
        .then(res => {
          // console.log(res.data)
        })

      that.choice = []
      d3.selectAll('rect').attr('stroke-width', 0.6).attr('stroke', 'black')
      d3.selectAll('circle').remove()
      d3.selectAll('line').remove()
      d3.selectAll('rect').remove()
      that.restart()
    },
    onClick: function(event) {
      if (event.keyCode == '13') {
        var that = this
        clearTimeout(that.timer)
        that.time = Date.now() - that.startTime
        const params = new URLSearchParams()
        // username, gender, age, layout, path, groupSize, file, answer, time
        let now = new Date()
        let date = '' + now.getFullYear() + (now.getMonth() + 1) + now.getDate() + now.getHours() + now.getMinutes()
        params.set('date', date)
        params.set('userName', that.$parent.userName)
        params.set('gender', that.$parent.gender)
        params.set('age', that.$parent.age)
        params.set('layout', that.graph.layout)
        params.set('level', that.$parent.level)
        let nodeHistoryString = ""
        for (let i=0; i<that.nodeHistory.length; ++i){
          if (i != 0) {
            nodeHistoryString += " "
          }
          nodeHistoryString += "" + that.nodeHistory[i]
        }
        params.set('nodeHistory', nodeHistoryString)
        let pathString = ""
        for (let i=0; i<that.selectedNodes.length; ++i){
          if (i != 0) {
            pathString += " "
          }
          pathString += "" + that.selectedNodes[i]
        }
        params.set('path', pathString)
        params.set('path_length_difference', that.graph.shortest_path.length - that.selectedNodes.length)
        params.set('groupSize', that.graph.groupSize)
        params.set('origin_filename', '' + that.graph.file)
        params.set('filename', '' + that.graph.arranged_filename)
        if (that.checkAnswer() == 1){
          that.answer = 1
        } else {
          that.answer = 0
        }
        params.set('answer', that.answer)
        params.set('time', that.time)
        console.log(params)
        const url = `http://127.0.0.1:5000/data/${params.toString()}`
        axios.get(url)
          .then(res => {
            // console.log(res.data)
          })

        that.choice = []
        d3.selectAll('rect').attr('stroke-width', 0.6).attr('stroke', 'black')
        d3.selectAll('circle').remove()
        d3.selectAll('line').remove()
        d3.selectAll('rect').remove()
        that.restart()
      }
    },
    reLinks: function() {
      var that = this;
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "links")
          .selectAll("line")
          .data(that.graph.links)
          .enter().append("line")
          .attr("stroke-width", function(d) {
            // return Math.sqrt(d.value);
            return 0.4;
          })
          .attr('stroke', function(d) {
            return d3.rgb(100, 100, 100)
          })
        d3.selectAll("line")
          .each(function(d, i) {
            var selection = d3.select(this)
            selection.attr('x1', function(d) {
                return that.graph.nodes[d.source].cx
              })
              .attr('y1', function(d) {
                return that.graph.nodes[d.source].cy
              })
              .attr('x2', function(d) {
                return that.graph.nodes[d.target].cx
              })
              .attr('y2', function(d) {
                return that.graph.nodes[d.target].cy
              })
          })
        d3.selection.prototype.moveToFront = function() {
          return this.each(function() {
            this.parentNode.parentNode.appendChild(this.parentNode);
          })
        }
        d3.select('circle').moveToFront()
        return d3.selectAll("line")
      }
    },
    reBoxes: function() {
      var that = this
      if (that.graph) {
        d3.select("svg").append("g")
          .attr("class", "rect")
          .selectAll("rect")
          .data(that.graph.groups)
          .enter().append("rect")
          .attr("stroke", "black")
          .attr("stroke-width", 1)
          .attr("fill", 'transparent')

        function func(event) {
          d3.selectAll('rect')
            .each(function(d, i) {
              if (event.x == d.x && event.y == d.y) {
                var selection = d3.select(this)
                if (selection.attr('stroke') == 'black') {
                  d3.selectAll('rect')
                    .attr("stroke-width", 1)
                    .attr('stroke', 'black')
                  this.parentNode.appendChild(this)
                  selection.attr("stroke-width", 3)
                    .attr('stroke', d3.rgb(102, 200, 255))
                  for (let i in that.graph.groups) {
                    if (event.x == that.graph.groups[i].x && event.y == that.graph.groups[i].y) {
                      that.choice = [i]
                      break
                    }
                  }
                } else if (selection.attr('stroke') == d3.rgb(102, 200, 255)) {
                  selection.attr("stroke-width", 1)
                    .attr('stroke', 'black')
                  let tmp
                  for (let i in that.graph.groups) {
                    if (event.x == that.graph.groups[i].x && event.y == that.graph.groups[i].y) {
                      tmp = i
                      break
                    }
                  }
                  for (let i in that.choice) {
                    if (tmp == that.choice[i]) {
                      that.choice.splice(i, 1)
                    }
                  }
                }
              }
            })
        }
        return d3.selectAll('rect')
          .each(function(d, i) {
            if (d['dx'] != that.settings.svgWigth || d['dy'] != that.settings.svgHeight) {
              var selection = d3.select(this)
                .attr('index', i)
                .attr('x', d['x'])
                .attr('y', d['y'])
                .attr('width', d['dx'])
                .attr('height', d['dy'])
                // .on('click', func)
            }
          })
      }
    },
    autoCheck: function() {
      let that = this
      if (that.checkAnswer()) {
        d3.selectAll('line')
          .each(function(d, i) {
            let selection = d3.select(this)
            if ((that.selectedNodes.indexOf(d.source) >= 0) && (that.selectedNodes.indexOf(d.target) >= 0)) {
              selection.attr('stroke', that.answerColor)
              selection.attr('opacity', 1.)
              selection.attr('stroke-width', 2 * that.twosideThickness)
            }
          })
        that.autoCorrect()
      }
    },
    selectNode: function(d, i){
      let that = this
      let preference = d.name
      let select_number = d.id
      that.nodeHistory.push(d.id)
      if (that.selectedNodes.indexOf(d.id) < 0){
        let relLinks = []
        let relNodes = []
        for (let i=0; i < that.graph.links.length; i++){
          if ((d.name === that.graph.links[i].source) || (d.name === that.graph.links[i].target)){
            relLinks.push(that.graph.links[i])
          }
        }
        for (let n=0; n < relLinks.length; n++){
          if (relLinks[n].source === d.name){
            relNodes.push(relLinks[n].target)
          } else if (relLinks[n].target === d.name){
            relNodes.push(relLinks[n].source)
          }
        }
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if (relLinks.length !== 0) {
              for (let n=0; n<relNodes.length; n++){
                if (nd.name == relNodes[n]) {
                  that.relatedNodes[parseInt(relNodes[n])].push(select_number)
                  if (that.selectedNodes.indexOf(nd.id) < 0){
                    selection.attr('r', that.relatedSize)
                  }
                }
                else if (nd.name === preference) {
                  if (that.selectedNodes.indexOf(nd.id) < 0){
                    that.selectedNodes.push(nd.id)
                  }
                  selection.attr('r', that.selectSize)
                  if (that.graph.shortest_path.nodes.indexOf(nd.id) >= 0) {
                    selection.attr('fill', that.twosideColor)
                    selection.attr('stroke', that.givenNodesColors[that.graph.shortest_path.nodes.indexOf(nd.id)])
                    selection.attr('stroke-width', that.givenNodesStrokeWidth)
                  } else {
                    let count = 0
                    for (let i=0; i<2; i++) {
                      if (that.selectedNodes.indexOf(that.graph.shortest_path.nodes[i]) >= 0) {
                        count += 1
                      }
                    }
                    selection.attr('fill', that.colors[that.selectedNodes.indexOf(nd.id) - count])
                  }
                  // selection.attr('stroke', 'yellow')
                  // selection.attr('stroke-width', 3)
                }
              }
            } else if (nd.name === preference) {
              selection.attr('r', that.selectSize)
              // selection.attr('stroke', 'yellow')
              // selection.attr('stroke-width', 3)
              if (that.selectedNodes.indexOf(nd.id) < 0){
                that.selectedNodes.push(nd.id)
              }
            }
          })
        d3.selectAll('line')
          .each(function(ld, li){
            let selection = d3.select(this)
            for (let n=0; n<relLinks.length; n++){
              if (relLinks[n].id === ld.id){
                that.onesideLinks[parseInt(ld.id)].push(parseInt(select_number))
                selection.lower()

                let order = that.graph.shortest_path.nodes.indexOf(ld.source)
                if (that.graph.shortest_path.nodes.indexOf(ld.target) > order) {
                  order = that.graph.shortest_path.nodes.indexOf(ld.target)
                }
                if (order >= 0) {
                  selection.attr('stroke', that.givenNodesColors[order])
                  selection.attr('stroke-width', that.onesideThickness)
                  selection.attr('opacity', that.linkOpacity) 
                } else {
                  let count = 0
                  for (let i=0; i<2; i++) {
                    if (that.selectedNodes.indexOf(that.graph.shortest_path.nodes[i]) >= 0) {
                      count += 1
                    }
                  }
                  selection.attr('stroke', that.colors[that.selectedNodes.indexOf(d.id) - count])
                  selection.attr('stroke-width', that.onesideThickness)
                  selection.attr('opacity', that.linkOpacity) 
                }
              }
            }
          })
        d3.selectAll('line')
          .each(function(ld, li){
            let selection = d3.select(this)
            for (let n=0; n<relLinks.length; n++){
              if (relLinks[n].id === ld.id){
                if ((that.selectedNodes.indexOf(relLinks[n].source) >= 0) && ((that.selectedNodes.indexOf(relLinks[n].target) >= 0))) {
                  let _list = [relLinks[n].source, relLinks[n].target]
                  that.twosideLinks[parseInt(ld.id)].push(_list)
                  selection.raise()
                  selection.attr('stroke', that.twosideColor)
                  selection.attr('stroke-width', that.twosideThickness)
                  selection.attr('opacity', that.linkOpacity)
                }
              }
            }
          })
      } else {
        let rmList = []
        for (let n=0; n<that.selectedNodes.length; n++){
          if (that.selectedNodes[n] === preference){
            let front = that.selectedNodes.slice(0, n)
            let back = that.selectedNodes.slice(n+1, that.selectedNodes.length)
            that.selectedNodes = front.concat(back)
          }
        }
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if (nd.id === select_number){
              selection.attr('r', that.normalSize)
              selection.attr('stroke-width', 0)
              if (that.graph.shortest_path.nodes.indexOf(nd.id) >= 0) {
                selection.attr('fill', that.twosideColor)
              } else {
                selection.attr('fill', 'black')
              }
            } else {
              for(let n=0; n < that.relatedNodes.length; n++){
                let order = that.relatedNodes[n].indexOf(select_number)
                if (order > -1){
                  let front = that.relatedNodes[n].slice(0, order)
                  let back = that.relatedNodes[n].slice(order+1, that.relatedNodes[n].length)
                  that.relatedNodes[n] = front.concat(back)
                  if ((that.relatedNodes[n].length === 0) && (that.selectedNodes.indexOf(that.graph.nodes[n].id) < 0)){
                    rmList.push(n)
                  }
                }
              }
            }
          })
        d3.selectAll("circle")
          .each(function(nd, ni) {
            var selection = d3.select(this)
            if (rmList.indexOf(nd.id) > -1){
              selection.attr('r', that.normalSize)
            }
        })
        // reomve twoside links
        for (let n=0; n<that.onesideLinks.length; n++){
          let order = that.onesideLinks[n].indexOf(select_number)
          if (order > -1) {
            let front = that.onesideLinks[n].slice(0, order)
            let back = that.onesideLinks[n].slice(order + 1, that.onesideLinks[n].length)
            that.onesideLinks[n] = front.concat(back)
          }
        }
        // reomve oneside links
        for (let n=0; n<that.twosideLinks.length; n++){
          for (let m=0; m<that.twosideLinks[n].length; m++) {
            if (that.twosideLinks[n].length > 0) {
            }
            if (that.twosideLinks[n][m].indexOf(select_number) >= 0) {
              let front = that.twosideLinks[n].slice(0, m)
              let back = that.twosideLinks[n].slice(m + 1, that.twosideLinks[n][m].length)
              that.twosideLinks[n] = front.concat(back)
            }
          }
        }
        d3.selectAll('line').each(function(ld, li) {
          let selection = d3.select(this)
          if ((that.onesideLinks[parseInt(ld.id)].length != 0) && (that.twosideLinks[ld.id].length == 0)) {
            if (that.graph.shortest_path.nodes.indexOf(that.onesideLinks[ld.id][0]) >= 0) {
              selection.attr('stroke', that.givenNodesColors[that.graph.shortest_path.nodes.indexOf(that.onesideLinks[ld.id][0])])
              selection.attr('stroke-width', that.onesideThickness)
            } else {
              let count = 0
              for (let i=0; i<2; i++) {
                if (that.selectedNodes.indexOf(that.graph.shortest_path.nodes[i]) >= 0) {
                  count += 1
                }
              }
              selection.attr('stroke', that.colors[that.selectedNodes.indexOf(that.onesideLinks[ld.id][0]) - count])
              selection.attr('stroke-width', that.onesideThickness)
            }
          }
          else if ((that.onesideLinks[parseInt(ld.id)].length === 0) && (that.twosideLinks[ld.id].length == 0)){
            selection.attr('stroke', d3.rgb(100, 100, 100))
            selection.attr('stroke-width', 0.4)
          }
        })
      }
      that.autoCheck()
    },
    initialEdgeNodesHighliht: function(){
      let that = this
      d3.selectAll("circle")
        .each(function(d, i) {
          if (that.selectedNodes.indexOf(d.id) >= 0) {
            let selection = d3.select(this)
            selection.attr('r', that.selectSize)
            // selection.attr('stroke', 'yellow')
            // selection.attr('stroke-width', 3)

            let relLinks = []
            let relNodes = []
            for (let i=0; i < that.graph.links.length; i++){
              if ((d.id === that.graph.links[i].source) || (d.id === that.graph.links[i].target)){
                relLinks.push(that.graph.links[i])
              }
            }
            for (let n=0; n < relLinks.length; n++){
              if (relLinks[n].source === d.id){
                relNodes.push(relLinks[n].target)
                that.relatedNodes[relLinks[n].target].push(d.id)
              } else if (relLinks[n].target === d.id){
                relNodes.push(relLinks[n].source)
                that.relatedNodes[relLinks[n].source].push(d.id)
              }
            }
            d3.selectAll("circle")
              .each(function(nd, ni) {
                let _selection = d3.select(this)
                if ((relNodes.indexOf(nd.id) >= 0) && (that.selectedNodes.indexOf(nd.id) < 0)) {
                  _selection.attr('r', that.relatedSize)
                } else if (that.selectedNodes.indexOf(nd.id) >= 0) {
                  _selection.attr('stroke', that.givenNodesColors[that.graph.shortest_path.nodes.indexOf(nd.id)])
                  _selection.attr('stroke-width', that.givenNodesStrokeWidth)
                }
              })
            d3.selectAll('line')
              .each(function(ld, li){
                let _selection = d3.select(this)
                for (let i=0; i<relLinks.length; ++i) {
                  if (relLinks[i].id == ld.id) {
                    that.onesideLinks[parseInt(ld.id)].push(parseInt(d.id))
                    _selection.lower()
                    _selection.attr('stroke',  that.givenNodesColors[that.graph.shortest_path.nodes.indexOf(d.id)])
                    _selection.attr('stroke-width', that.onesideThickness)
                    _selection.attr('opacity', that.linkOpacity)
                  }
                }
              })
          }
      })
    }
  },
}
</script>


<style>
body {
  margin: auto;
  width: 100%;
  height: 100%;
  font-family: 'serif';
}

.app {
  margin: auto;
  width: 85%;
  height: 100%;
  font-family: 'serif';
}

.controls {
  text-align: center;
  width: 80%;
  margin: auto;
  padding-bottom: 2rem;
  margin-top: 2rem;
  /* margin: auto; */
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.sync {
  background: black;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
}

.text {
  width: 80%;
  margin: auto;
  text-align: center;
  margin-top: 20%;
  font-size: 1.3rem;
}

.el-aside {
  /* border: 1px solid #67C23A; */
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
}

.el-header {
  margin-bottom: 5%;
}

.el-main {
  box-shadow: 1px 2px 4px rgba(0, 0, 0, .5);
  text-align: center;
}

.svg-container {
  margin: auto;
  display: table;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}

label {
  display: block;
}

.links line {
  /*stroke: #999;*/
  /*opacity: 1;*/
}

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
