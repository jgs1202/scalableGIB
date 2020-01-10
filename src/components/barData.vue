<script>
import {Bar} from 'vue-chartjs'
export default {
  name: 'barData',
  extends: Bar,
  data: function() {
    return {
      data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
          // label: "move of AOI",
          // data: [10, 20, 30, 40, 50, 30],
          // backgroundColor: ['rgba(255, 99, 132, 0.2)',
          //                   'rgba(54, 162, 235, 0.2)',
          //                   'rgba(255, 206, 86, 0.2)',
          //                   'rgba(75, 192, 192, 0.2)',
          //                   'rgba(153, 102, 255, 0.2)',
          //                   'rgba(255, 159, 64, 0.2)'],
          // borderColor: ['rgba(255, 99, 132, 1)',
          //               'rgba(54, 162, 235, 1)',
          //               'rgba(255, 206, 86, 1)',
          //               'rgba(75, 192, 192, 1)',
          //               'rgba(153, 102, 255, 1)',
          //               'rgba(255, 159, 64, 1)'],
          // borderWidth: 1
          {label: "1~10位", data: [10, 9, 20], backgroundColor: 'rgba(255, 99, 132, 0.2)'},
          {label: "11~10位", data: [20, 6, 30], backgroundColor: 'rgba(54, 162, 235, 0.2)'},
          {label: "21~10位", data: [30, 12, 40], backgroundColor: 'rgba(255, 206, 86, 0.2)'},
          {label: "31~50位", data: [40, 8, 40], backgroundColor: 'rgba(75, 192, 192, 0.2)'},
          {label: "51~100位", data: [60, 6, 60], backgroundColor: 'rgba(153, 102, 255, 0.2)'},
        ],
      },
      options: {
        plugins: {
          stacked100: {enable: true},
        },
        title: {
          display: true,
          text: "move of AOIs"
        },
        scales: {
          xAxes: [{
            stacked: true,
            categoryPercentage: 0.5,
            barPercentage: 1
          }],
          yAxes: [{
              stacked: true,
              display: true,
              scaleLabel: {
                display: true,
                fontSize: 18
              },
              ticks: {
                min: 0,
                max: 100,
                fontSize: 18,
                stepSize: 20
              }
          }]
        },
        legend: {
          display: true
        }
      },
    }
  },
  mounted: function() {
    this.renderChart(this.data, this.options)
  },
  methods: {
  }
}
</script>

<style>
</style>
