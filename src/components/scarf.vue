<template>
<div>
  <div id="app" class="app">
    <el-container>
      <el-aside width='20%'>
        <div class="controls">
          <br>
          <label>Adjust width</label>
          <el-slider v-model="settings.width"></el-slider>
        </div>
        <div id="selectQue" style="margin-left: auto;">
          <div id='question'>
            <div class="previousAndNext">
              <el-button v-on:click='previousQue'>Previous</el-button>
              <el-button v-on:click='nextQue'>Next</el-button>
            </div>
            <span class='queNumber'>
              Question:
              <el-input placeholder="question number" v-model="queNum" style='width:3rem;'></el-input>
            </span>
          </div>
          <el-button v-on:click='reload'>Select</el-button>
        </div>
        <div id='information' style='margin-left: auto;'>
          <span>accuracy: {{accuracy}}</span><br><br>
          <span>completion time: {{meanTime}}</span><br><br>
          <span>layout: {{layout}}</span>
        </div>
      </el-aside>
      <el-main>
        <div class="svg-container" :style="{width: settings.width + '%'}">
          <svg id="svg" pointer-events="all" viewBox="0 0 960 600" preserveAspectRatio="xMinYMin meet">
          </svg>
        </div>
      </el-main>
    </el-container>
  </div>
  <div id="load" style='margin-top: auto; padding-top: 30%;'>
    loading...
  </div>
</div>
</template>

<script>
const d3 = require('d3')
export default {
  name: 'scarf',
  data: function() {
    return {
      settings: {
        strokeColor: "#29B5FF",
        width: 100,
        svgWigth: 960,
        svgHeight: 600
      },
      abstinfo: null,
      scarfData: null,
      choice: [],
      dataArray: [],
      dataNum: 0,
      dataMax: 120,
      task: [],
      taskNum: 0,
      queNum: 0,
      maxQue: 120,
      maxTask: 3,
      accuracy: null,
      meanTime: null,
      layout: null,
    }
  },
  mounted: function() {
    var that = this;
    document.getElementById('app').style.display = 'none'
    d3.json("./src/data/eye-tracking/abst_info.json").then(function(data1) {
      that.abstinfo = data1
      d3.json("./src/data/eye-tracking/segmentedFixation.json").then(function(data2) {
        console.log('load end')
        that.scarfData = data2
        that.loadEnd()
      })
    })
  },
  methods: {
    loadEnd: function() {
      document.getElementById('load').style.display = 'none'
      document.getElementById('app').style.display = 'block'
    },
    previousQue: function() {
      let that = this
      if (that.queNum != 0){
        that.queNum = parseInt(that.queNum) - 1
        that.reload()
      }
    },
    nextQue: function() {
      let that = this
      if (that.queNum != that.maxQue){
        that.queNum = parseInt(that.queNum) + 1
        that.reload()
      }
    },
    reload: function() {
      d3.selectAll('rect').remove()
      d3.selectAll('line').remove()
      d3.selectAll('text').remove()
      var that = this;
      let scarf = {}
      scarf.data = that.scarfData[that.queNum]
      scarf.segmentsLength = 1000
      scarf.colors = []
      scarf.groupSize = that.abstinfo[that.queNum].groupSize
      scarf.margin_left = 100
      scarf.margin_top = 20
      scarf.width = 700
      scarf.height = 570
      scarf.eachHeight = scarf.height / scarf.data.length - 10
      let a = [0]
      let b = [0, 1]

      that.accuracy = Math.round(parseInt(that.abstinfo[that.queNum].correct) / parseInt(that.abstinfo[that.queNum].people) * 1000) / 10
      that.meanTime = Math.round(parseInt(that.abstinfo[that.queNum].meanTime))
      that.layout = that.abstinfo[that.queNum].layout

      scarf.legend = {}
      scarf.legend.left = 850
      scarf.legend.top = 180
      scarf.legend.width = 50
      scarf.legend.height = 300
      scarf.maxAOIMove = 20
      scarf.colorNoFixation = 'green'
      scarf.numberofPeople = scarf.data.length

      for(let person=0; person<scarf.data.length; person++){
        d3.select('svg').append('g')
          .attr('class', 'canpas')
          .selectAll('rect')
          .data(scarf.data[person].segments)
          .enter()
          .append('rect')
          .attr('x', function(d, num){
              return scarf.margin_left + num * scarf.width / scarf.segmentsLength
          })
          .attr('y', function(d, num){
              return scarf.margin_top + person / scarf.numberofPeople * scarf.height
          })
          .attr('width', function(d, num){
              return scarf.width / scarf.segmentsLength
          })
          .attr('height', function(d, num){
              return scarf.eachHeight
          })
          .attr('stroke', function(d, num){
              if (scarf.data[person].segments[num].fixation == true) {
                return d3.interpolateYlOrBr(1 - (parseInt(scarf.data[person].segments[num].AOIsAfter) + parseInt(scarf.data[person].segments[num].AOIsBefore)) / 30)
              } else {
                return scarf.colorNoFixation
              }
          })
          .attr('stroke-width', '0.4')
          .attr('fill', function(d, num){
              if (scarf.data[person].segments[num].fixation == true) {
                return d3.interpolateYlOrBr(1 - (parseInt(scarf.data[person].segments[num].AOIsAfter) + parseInt(scarf.data[person].segments[num].AOIsBefore)) / 30)
              } else {
                return scarf.colorNoFixation
              }
          })

        d3.select('svg').append('g')
          .attr('class', 'participants')
          .selectAll('text')
          .data(a)
          .enter().append("text")
          .text('participants ' + ''  + person)
          .attr('x', scarf.margin_left / 10)
          .attr('y', scarf.margin_top + person / scarf.data.length * scarf.height + scarf.eachHeight / 4 * 3)
          .attr("font-family", "sans-serif")
          .attr("font-size", "12px")
          .attr("fill", function(d, i) {
            console.log(scarf.data[person])
              if (scarf.data[person].answer == 1) {
                return 'blue'
              } else {
                return 'red'
              }
          })
      }

      d3.select('svg').append('g')
        .attr('class', 'legend')
        .selectAll('rect')
        .data(scarf.data[0].segments)
        .enter()
        .append('rect')
        .attr('x', scarf.legend.left)
        .attr('y', function(d, num){
          return scarf.legend.top + num * scarf.legend.height / scarf.segmentsLength
        })
        .attr('width', scarf.legend.width)
        .attr('height', scarf.legend.height / scarf.segmentsLength)
        .attr('stroke', function(d, num){
          return d3.interpolateYlOrBr((num) / scarf.segmentsLength)
        })
        .attr('stroke-width', '0.4')
        .attr('fill', function(d, num){
          return d3.interpolateYlOrBr((num) / scarf.segmentsLength)
        })

      let AOILegendsHeights = []
      let numberOfLegends = 6
      for (let i=0; i<numberOfLegends; i++) {
        AOILegendsHeights.push(scarf.maxAOIMove - i * scarf.maxAOIMove / (numberOfLegends - 1))
      }
      d3.select('svg').append('g')
          .attr('class', 'AOIMoveNumber')
          .selectAll('text')
          .data(AOILegendsHeights)
          .enter().append("text")
          .text(function(d, num){
            console.log('' + AOILegendsHeights[num])
            return '' + AOILegendsHeights[num]
          })
          .attr('x', scarf.legend.left + scarf.legend.width * 1.5)
          .attr('y', function(d, num){
            return scarf.legend.top + num * scarf.legend.height / (numberOfLegends - 1) + 8
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black")

        d3.select('svg').append('g')
          .attr('class', 'AOI_title')
          .selectAll('text')
          .data(a)
          .enter().append("text")
          .text('AOIs')
          .attr('x', scarf.legend.left + 6)
          .attr('y', function(d, num){
            return scarf.legend.top - 10
          })
          .attr("font-family", "sans-serif")
          .attr("font-size", "16px")
          .attr("fill", "black");
      console.log('draw end')
    },
  },
}
</script>


<style>
.controls {
  text-align: center;
  width: 80%;
  margin: auto;
  padding-bottom: 10px;
  margin-top: 2rem;
  /* margin: auto; */
  background: #f8f8f8;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
}

.svg-container {
  position: relative;
  height: 100%;
  /* display: table; */
  margin: auto;
  border: 0px solid #f8f8f8;
  /* box-shadow: 1px 2px 4px rgba(0, 0, 0, .5); */
}

.controls>*+* {
  margin-top: 1rem;
  font-size: 1rem;
}

.controls > .el-button {
  width: 4rem;
}

.queNumber {
  padding-left: 0.1rem;
  padding-right: 1rem;
}

.question {
  margin: auto;
  text-align: center;
}

.container {
  text-align: center;
}

#question {
  margin-bottom: 1rem;
}

#question > .el-button {
  width: 5.5rem;
}

.previousAndNext {
  margin-bottom: 1rem;
}

#selectQue {
  margin-top: 2rem;
  margin-bottom: 2rem;
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

/*.nodes circle {
  stroke: #fff;
  stroke-width: 1.0px;
}*/
</style>
