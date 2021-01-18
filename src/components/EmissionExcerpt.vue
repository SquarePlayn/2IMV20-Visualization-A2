<template>
  <!--  <b-row>
      <b-col class="emission-excerpt">
        Emission chart excerpt at current time will go here.
      </b-col>
    </b-row>-->
  <div>
    <highcharts class="hc" :options="chartOptions" ref="chart"></highcharts>
  </div>
</template>

<script>
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import { utility } from "../mixins/utility";
import * as topojson from "topojson/dist/topojson";

stockInit(Highcharts)

// Get the data of the selected day
//const dateFormatted = this.formatDate(this.time);
//const dateData = this.data[dateFormatted];


export default {
  name: "EmissionExcerpt",
  props: ['data', 'settings', 'time'],
  mixins: [utility],
  data() {
    return {
      chartOptions: {
        chart: {
          type: "column",
        },
        title: {
          text: "CO2 emission per sector",
        },
        yAxis: {
          title: {
            text: "CO2 emission",
          },
        },
        xAxis: {
          min: 0,
          categories: ["Power", "Ground Transport", "Industry", "Residential", "Domestic Aviation"],
          title: {
            text: "Sector",
            align: "high",
          },
          labels: {
            overflow: "justify",
          },
        },
        tooltip: {
          valueSuffix: " millions",
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        legend: {
          layout: "vertical",
          align: "right",
          verticalAlign: "top",
          x: -40,
          y: 80,
          floating: true,
          borderWidth: 1,
          backgroundColor:
              (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || "#FFFFFF",
          shadow: true,
        },
        credits: {
          enabled: false,
        },
        series: [
          {
            data: [107, 31, 635, 203, 2,],
          },
        ],
      },
    };
  },

  watch: {
    time: 'updateChart',
  },

  methods: {
    updateChart(){

      const dateFormatted = this.formatDate(this.time);
      console.log(dateFormatted);
      const dateData = this.data[dateFormatted];
      console.log((dateData['Brazil'])['Emissions']);
      this.chartOptions.series[0].data = [125,39, 78, 100, 89];
      console.log(this.settings.country.selected);
    },

  },

};
</script>

<style scoped>
.emission-excerpt {
  background-color: deepskyblue;
  height: 48vh;
}
</style>