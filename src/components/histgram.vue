<template>
<div>
  <div id="app" class="app">
    <el-container>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
            <g id="nodes">{{nodes}}</g>
            <g id="links">{{links}}</g>
            <g id='boxes'>{{boxes}}</g>
            <g id='traje'>{{traje}}</g>
            <g id='hist'>{{hist}}</g>
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
  name: 'histgram',
  data: function() {
    return {
      graph: null,
      simulation: null,
      // color: d3.scaleOrdinal(d3.interpolateRainbow),
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      nodes: [],
      links: [],
      boxes: [],
      choice: [],
      dataNum: 0,
      dataMax: 120,
      options: [],
      radio: null,
      startTime: null,
      time: null,
      answer: null,
      abstData: null,
      segmentsNumber: 1000,
      timeSerieseAOIData: null,
      trajes: [],
      traje: [],
      hists: [],
      hist: [],
      accuracy: null,
      meanTime: null,
      drag: null,
    }
  },
  mounted: function() {
    var that = this;
    that.drag = d3.drag()
      .on("drag", function(d,i) {
          console.log(d)
          console.log(d[0], d[1])
          d[0] += d3.event.dx;
          d[1] += d3.event.dy;
          d3.select(this).attr("transform", function(d,i){
              return "translate(" + [ d[0], d[1] ] + ")";
          });
      });
    d3.json('./src/data/eye-tracking/abst_info.json').then(function(data) {
      that.abstData = data
      d3.json('./src/data/eye-tracking/timeSeriesePlotData.json').then(function(graph) {
        that.timeSerieseAOIData = graph
        console.log('data loaded')
        that.restart()
        window.addEventListener('keyup', that.onClick)
      })
    })
  },
  methods: {
    restart: function() {
      var that = this;
      console.log('data number is ' + '' + that.dataNum)
      if ((that.dataNum != 0) &&(that.dataNum % that.dataMax == 0)) {
        this.$parent.currentPage = 'Menu'
      }
      d3.json("./src/data/random/" + '' + that.dataNum + ".json").then(function(graph) {
        that.graph = graph
        that.graph.groups.pop()
        that.$set(that.nodes, that.reNodes())
        that.$set(that.boxes, that.reBoxes())
        that.$set(that.links, that.reLinks())
        that.reHist()
        that.abstinfo()
      })
    },
    reHist: function(dataNum) {
      console.log('hist calculation')
      var that = this
      let hist = {}
      let isFDGIB = (that.graph.layout == 'FDGIB')
      let hist_width, hist_height
      if (isFDGIB) {
        hist_width = 50
        hist_height = 30
      } else {
        hist_width = 100
        hist_height = 50
      }
      hist.data = that.timeSerieseAOIData[that.dataNum]
      hist.plotData = Array(that.graph.gruopSize)
      for (let i=0; i<that.graph.groupSize; i++){
        hist.plotData[i] = Array(that.segmentsNumber)
        for (let j=0; j<that.segmentsNumber; j++){
          hist.plotData[i][j] = Array(2)
          hist.plotData[i][j][0] = j
          hist.plotData[i][j][1] = parseFloat(hist.data[i][j])
        }
        let a = [0]
        d3.select('svg').append('g')
          .attr('class', 'canpas')
          .selectAll('rect')
          .data(a)
          .enter()
          .append('rect')
          .attr('x', parseInt(that.graph.groups[i].x) + 5)
          .attr('y', parseInt(that.graph.groups[i].y) + 5 - hist_height * isFDGIB / 2)
          .attr('width', hist_width)
          .attr('height', hist_height)
          .attr('stroke', 'black')
          .attr('stroke-width', '0.4')
          .attr('fill', 'white')
          .call(d3.drag()
            .subject(function(d) {return d})
            .on("start", function(d) {
              console.log(d)
              d3.event.sourceEvent.stopPropagation();
              d3.select(this).classed("dragging", true);
            })
            .on("drag", function(d) {
              console.log(this)
              d3.select(this).attr("x", d.x = d3.event.x).attr("y", d.y = d3.event.y)
            })
            .on("end", function(d) {
              d3.select(this).classed("dragging", false);
            }))
        d3.select('svg').append('g')
          .attr('class', 'bar')
          .selectAll('rect')
          .data(hist.plotData[i])
          .enter()
          .append('rect')
          .attr('x', function(d, num){
            return parseInt(that.graph.groups[i].x) + num * hist_width / 1000 + 5
          })
          .attr('y', function(d, num){
            return parseInt(that.graph.groups[i].y) + hist_height - hist.plotData[i][num][1] * hist_height + 5 - hist_height * isFDGIB / 2
        })
          .attr('width', hist_width / 1000)
          .attr('height', function(d, num){
            return hist.plotData[i][num][1] * hist_height
          })
          .attr('fill', d3.rgb(152, 0 ,192))
          .call(that.drag)
        d3.select('svg').append('g')
          .attr('class', 'border')
          .selectAll('line')
          .data(that.graph.links)
          .enter().append("line")
          .attr('stroke', 'black')
          .attr("stroke-width", 1.0)
          .attr('x1', that.graph.groups[i].x + 5)
          .attr('x2', that.graph.groups[i].x + hist_width + 5)
          .attr('y1', that.graph.groups[i].y + hist_height + 5 - hist_height * isFDGIB / 2)
          .attr('y2', that.graph.groups[i].y + hist_height + 5 - hist_height * isFDGIB / 2)
      }
    },
    abstinfo: function() {
      var that = this
      let tmp = that.abstData[that.dataNum]
      that.accuracy = Math.round(parseInt(tmp['correct']) / parseInt(tmp['people']) * 1000) / 10
      that.meanTime = Math.round(parseInt(tmp['meanTotalTime']))
      console.log(that.accuracy, that.meanTime)
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
          .attr("r", 3)
        return d3.selectAll("circle")
          .each(function(d, i) {
            var selection = d3.select(this)
            selection.transition()
              .attr('cx', that.graph.nodes[i].cx)
              .attr("cy", that.graph.nodes[i].cy)
              .attr("fill", function(d, i) {
                if (that.graph.shortest_path.nodes.indexOf(d.id) >= 0) {
                  return 'red'
                } else {
                  return 'black'
                }
              })
          })
      }
    },
    onClick: function(event) {
      if (event.keyCode == '13') {
        var that = this
        console.log('enter')
        // console.log(that.graph)
        d3.selectAll('rect').attr('stroke-width', 1).attr('stroke', 'black')
        d3.selectAll('circle').remove()
        d3.selectAll('line').remove()
        d3.selectAll('rect').remove()
        // that.graph = 0
        // d3.select('svg').remove()
        that.dataNum += 1
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
          .attr('stroke', d3.rgb(100, 100, 100))
          .attr('opacity', 0.6)
        d3.selectAll("line")
          .each(function(d, i) {
            // console.log('d is ')
            // console.log(d)
            if (d.source.x){
              var a = 0
            }
            else {
              var selection = d3.select(this)
              selection.attr('x1', function(d) {
                  // console.log(that.graph.nodes[d.source].cx)
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
              }
          })
        d3.selection.prototype.moveToFront = function() {
          return this.each(function() {
            this.parentNode.parentNode.appendChild(this.parentNode);
          })
        }
        d3.select('circle').moveToFront()
        return d3.selectAll('line')
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

        return d3.selectAll('rect')
          .each(function(d, i) {
            if (d['dx'] != that.settings.svgWigth || d['dy'] != that.settings.svgHeight) {
              var selection = d3.select(this)
                .attr('index', i)
                .attr('x', d['x'])
                .attr('y', d['y'])
                .attr('width', d['dx'])
                .attr('height', d['dy'])
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
  width: 95%;
  height: 95%;
  font-family: 'serif';
}

.svg-container {
  position: relative;
  height: 100%;
  /* display: table; */
  margin: auto;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
}

.question {
  margin: auto;
  text-align: center;
}

.container {
  text-align: center;
}

label {
  display: block;
}

.text {
  width: 80%;
  margin: auto;
  text-align: center;
  margin-top: 20%;
  font-size: 1.3rem;
}
.el-radio {
  width: 40%;
}

.sync {
  background: black;
  height: 60px;
  width: 60px;
  position: absolute;
  right: 0;
  bottom: 0;
}

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
