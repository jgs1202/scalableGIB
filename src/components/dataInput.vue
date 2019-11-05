<template>
<el-container>
  <el-header>
    <div class="title">
      GIB Experiment
    </div>
  </el-header>
  <el-main>
    <div id="dataInput">
      <div class="dataInput">
        <table align="center">
          <tr>
            <td>
              <el-input placeholder="Please input" v-model="userName">
                <template slot="prepend">Name</template>
              </el-input>
            </td>
          </tr>
          <tr>
            <td>
              <el-input placeholder="Please input" v-model="age">
                <template slot="prepend">Age</template>
              </el-input>
            </td>
          </tr>
          <tr>
            <td>
              <div class="row">
                <el-radio v-model="gender" label="Male" border>Male</el-radio>
                <el-radio v-model="gender" label="Female" border>Female</el-radio>
              </div>
            </td>
          </tr>
          <tr>
            <td>
              <div class="row">
                <el-button type="primary" v-on:click='send'>Send Data</el-button>
              </div>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </el-main>
</el-container>
</template>

<script>
export default {
  name: 'dataInput',
  data: function() {
    return {
      userName: null,
      age: null,
      gender: "Male",
    }
  },
  methods: {
    send: function(event) {
      this.$parent.currentPage = 'Menu'
      this.$parent.userName = this.userName
      this.$parent.age = this.age
      this.$parent.gender = this.gender
    }
  }
}
</script>

<style>
body {
  margin-top: 4rem;
  width: 95%;
  height: 95%;
  font-family: 'serif';
  text-align: center;
}

.el-container {
  position: relative;
  margin-top: 30px;
}

table {
  border-collapse: separate;
  border-spacing: 0px 15px;
}

td {
  margin-top: 20px;
}

.el-row {
  text-align: center;
  margin-top: 0px;
  margin-bottom: 0px;
}

.title {
  font-size: 2rem;
}

.row {
  margin-top: 15px;
  margin-bottom: 12px;
}

.mini {
  margin-top: 60px;
}

.dataInput {
  margin: auto;
}
</style>
