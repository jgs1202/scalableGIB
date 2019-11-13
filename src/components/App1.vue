<template>
<div>
  <div id="app" class="app">
    <el-container>
      <!-- <el-aside width='20%'>
        <div class='text'>
          Which box does have the most intra-links?<br><br>
          グループ内リングか一番多いものを選んでください。
        </div>
        <div class="controls">
          <br>
          <label>Adjust width</label>
          <el-slider v-model="settings.width"></el-slider>
        </div>
      </el-aside> -->
      <el-main> 
        {{level}} - {{file}} <br><br>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
      <g id="nodes">{{nodes}}</g>
      <g id="links">{{links}}</g>
      <g id='boxes'>{{boxes}}</g>
    </svg>
        </div>
      </el-main>
    </el-container>
  </div>
  <div class="sync">
  </div>
</div>
</template>

<script>
import axios from 'axios'
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
      totalQue: 120,
      level: null,
      file: null,
      normalSize: 3,
      relatedSize: 5,
      selectSize: 7,
      selected: [],
      related: [],
      redLinks: [],
    }
  },
  mounted: function() {
    window.addEventListener('keyup', this.onClick)
    var that = this;
    if (that.$parent.level == 0){
      that.level = 'easy'
    } else if (that.$parent.level == 1) {
      that.level = 'difficult'
    }
    that.dataMax = that.$parent.total / 1
    d3.json("./src/data/" + that.$parent.levelIndex[that.$parent.level] + '/' + that.$parent.nums[that.$parent.level] + ".json").then(function(graph) {
      that.graph = graph
      that.related = []
      for (let i=0; i < that.graph.nodes.length; i++){
        that.related.push([])
      }
      that.redLinks = []
      for (let i=0; i < that.graph.links.length; i++){
        that.redLinks.push([])
      }
      that.graph.groups.pop()
      that.$set(that.boxes, that.reBoxes())
      that.$set(that.links, that.reLinks())
      that.$set(that.nodes, that.reNodes())
    })
    that.startTime = Date.now()
  },
  methods: {
    restart: function() {
      var that = this;
      that.$parent.nums[that.$parent.level] += 1
      console.log('num is ' + '' + that.$parent.nums[that.$parent.level])
      if (that.$parent.nums[that.$parent.level] % that.dataMax == 0) {
        this.$parent.already = 1
        this.$parent.currentPage = 'Menu'
      } else {
        d3.json("./src/data/" + that.$parent.levelIndex[that.$parent.level] + '/' + that.$parent.nums[that.$parent.level] + ".json").then(function(graph) {
          that.graph = graph
          that.related = []
          for (let i=0; i < that.graph.nodes.length; i++){
            that.related.push([])
          }
          that.redLinks = []
          for (let i=0; i < that.graph.links.length; i++){
            that.redLinks.push([])
          }
          that.graph.groups.pop()
          that.$set(that.boxes, that.reBoxes())
          that.$set(that.links, that.reLinks())
          that.$set(that.nodes, that.reNodes())
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
      }
    },
    reNodes: function() {
      var that = this;
      console.log('renodes')
      if (that.graph) {
        d3.selectAll('circle').remove()
        d3.select("svg").append("g")
          .attr("class", "nodes")
          .selectAll("circle")
          .data(that.graph.nodes)
          .enter().append("circle")
          .attr('cx', that.settings.svgWigth / 2)
          .attr('cy', that.settings.svgHeight / 2)
          .attr("r", 3)
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
                  return 'red'
                } else {
                  return 0.1
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
                if ((that.selected.indexOf(d) < 0) && (that.related[d.id].length === 0)){
                  selection.attr('r', that.normalSize)
                } else if ((that.selected.indexOf(d) < 0) && (that.related[d.id].length !== 0)){
                  selection.attr('r', that.relatedSize)
                }
              })
          })
      }
    },
    onClick: function(event) {
      if (event.keyCode == '13') {
        var that = this
        if (that.choice.length == 1) {
          that.time = Date.now() - that.startTime
          const params = new URLSearchParams()
          params.set('userName', this.$parent.userName)
          params.set('gender', this.$parent.gender)
          params.set('age', this.$parent.age)
          params.set('layout', that.graph.type)
          params.set('set', that.file)
          params.set('groupSize', that.graph.groupSize)
          params.set('file', '' + that.$parent.nums[that.$parent.level] + '.json')
          if (that.choice[0] == that.graph.linkMax){
            that.answer = 1
          } else {
            that.answer = 0
          }
          params.set('answer', that.answer)
          params.set('time', that.time)
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
                .on('click', func)
            }
          })
      }
    },
    selectNode: function(d, i){
      let that = this
      let preference = d.name
      let select_number = d.id
      if (that.selected.indexOf(d) < 0){
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
          .each(function(d, i) {
            var selection = d3.select(this)
            if (relLinks.length !== 0) {
              for (let n=0; n<relNodes.length; n++){
                if (d.name == relNodes[n]) {
                  that.related[parseInt(relNodes[n])].push(select_number)
                  if (that.selected.indexOf(d) < 0){
                    selection.attr('r', that.relatedSize)
                  }
                }
                else if (d.name === preference) {
                  selection.attr('r', that.selectSize)
                  selection.attr('stroke', 'yellow')
                  selection.attr('stroke-width', 3)
                  if (that.selected.indexOf(d) < 0){
                    that.selected.push(d)
                  }
                }
              }
            } else if (d.name === preference) {
              selection.attr('r', that.selectSize)
              selection.attr('stroke', 'yellow')
              selection.attr('stroke-width', 3)
              if (that.selected.indexOf(d) < 0){
                that.selected.push(d)
              }
            }
          })
        d3.selectAll('line')
          .each(function(d, i){
            let selection = d3.select(this)
            for (let n=0; n<relLinks.length; n++){
              if (relLinks[n].id === d.id){
                that.redLinks[parseInt(d.id)].push(parseInt(select_number))
                selection.attr('stroke', 'red')
                selection.attr('stroke-width', 1.5)
              }
            }
        })
      } else {
        let rmList = []
        for (let n=0; n<that.selected.length; n++){
          if (that.selected[n].name === preference){
            let front = that.selected.slice(0, n)
            let back = that.selected.slice(n+1, that.selected.length)
            that.selected = front.concat(back)
          }
        }
        d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            if (d.id === select_number){
              selection.attr('r', that.normalSize)
              selection.attr('stroke-width', 0)
            } else {
              for(let n=0; n < that.related.length; n++){
                let order = that.related[n].indexOf(select_number)
                if (order > -1){
                  let front = that.related[n].slice(0, order)
                  let back = that.related[n].slice(order+1, that.related[n].length)
                  that.related[n] = front.concat(back)
                  if ((that.related[n].length === 0) && (that.selected.indexOf(that.graph.nodes[n]) < 0)){
                    rmList.push(n)
                  }
                }
              }
            }
          })
        d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            if (rmList.indexOf(d.id) > -1){
              selection.attr('r', that.normalSize)
            }
        })
        // reomve red links
        for (let n=0; n<that.redLinks.length; n++){
          let order = that.redLinks[n].indexOf(select_number)
          if (order > -1) {
            let front = that.redLinks[n].slice(0, order)
            let back = that.redLinks[n].slice(order + 1, that.redLinks[n].length)
            that.redLinks[n] = front.concat(back)
          }
        }
        d3.selectAll('line').each(function(d, i) {
          let selection = d3.select(this)
          if (that.redLinks[parseInt(d.id)].length === 0){
            selection.attr('stroke', 'gray')
            selection.attr('stroke-width', 0.4)
          }
        })
      }
    },
    selectNode: function(d, i){
      let that = this
      let preference = d.name
      let select_number = d.id
      if (that.selected.indexOf(d) < 0){
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
          .each(function(d, i) {
            var selection = d3.select(this)
            if (relLinks.length !== 0) {
              for (let n=0; n<relNodes.length; n++){
                if (d.name == relNodes[n]) {
                  that.related[parseInt(relNodes[n])].push(select_number)
                  if (that.selected.indexOf(d) < 0){
                    selection.attr('r', that.relatedSize)
                  }
                }
                else if (d.name === preference) {
                  selection.attr('r', that.selectSize)
                  selection.attr('stroke', 'yellow')
                  selection.attr('stroke-width', 3)
                  if (that.selected.indexOf(d) < 0){
                    that.selected.push(d)
                  }
                }
              }
            } else if (d.name === preference) {
              selection.attr('r', that.selectSize)
              selection.attr('stroke', 'yellow')
              selection.attr('stroke-width', 3)
              if (that.selected.indexOf(d) < 0){
                that.selected.push(d)
              }
            }
          })
        d3.selectAll('line')
          .each(function(d, i){
            let selection = d3.select(this)
            for (let n=0; n<relLinks.length; n++){
              if (relLinks[n].id === d.id){
                that.redLinks[parseInt(d.id)].push(parseInt(select_number))
                selection.attr('stroke', 'red')
                selection.attr('stroke-width', 1.5)
              }
            }
        })
      } else {
        let rmList = []
        for (let n=0; n<that.selected.length; n++){
          if (that.selected[n].name === preference){
            let front = that.selected.slice(0, n)
            let back = that.selected.slice(n+1, that.selected.length)
            that.selected = front.concat(back)
          }
        }
        d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            if (d.id === select_number){
              selection.attr('r', that.normalSize)
              selection.attr('stroke-width', 0)
            } else {
              for(let n=0; n < that.related.length; n++){
                let order = that.related[n].indexOf(select_number)
                if (order > -1){
                  let front = that.related[n].slice(0, order)
                  let back = that.related[n].slice(order+1, that.related[n].length)
                  that.related[n] = front.concat(back)
                  if ((that.related[n].length === 0) && (that.selected.indexOf(that.graph.nodes[n]) < 0)){
                    rmList.push(n)
                  }
                }
              }
            }
          })
        d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            if (rmList.indexOf(d.id) > -1){
              selection.attr('r', that.normalSize)
            }
        })
        // reomve red links
        for (let n=0; n<that.redLinks.length; n++){
          let order = that.redLinks[n].indexOf(parseInt(select_number))
          if (order > -1) {
            let front = that.redLinks[n].slice(0, order)
            let back = that.redLinks[n].slice(order + 1, that.redLinks[n].length)
            that.redLinks[n] = front.concat(back)
          }
        }
        d3.selectAll('line').each(function(d, i) {
          let selection = d3.select(this)
          if (that.redLinks[parseInt(d.id)].length === 0){
            selection.attr('stroke', 'gray')
            selection.attr('stroke-width', 0.4)
          }
        })
      }
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
  width: 75%;
  height: 75%;
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
  stroke: #999;
  stroke-opacity: 1;
}

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
