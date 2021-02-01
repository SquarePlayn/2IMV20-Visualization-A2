<template>
   <b-row>
      <b-col class="emission-excerpt">
        <highcharts class="hc" :options="chartOptions" ref="chart"></highcharts>
      </b-col>
    </b-row>
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
  props: ['data', 'settings', 'time', 'selectedCountry'],
  mixins: [utility],
  data() {
    return {
      chartOptions: {
        chart: {
          type: "column",
        },
        title: {
          text: "CO2 emission per sector in the World " + this.formatDate(this.time),
        },
        yAxis: {
          title: {
            text: "CO2 emission",
            softMax: 90
          },
        },
        xAxis: {
          min: 0,
          categories: ["Power", "Ground Transport", "Industry", "Residential", "Domestic Aviation"],
          labels: {
            overflow: "justify",
          },
        },
        tooltip: {
          formatter: function() {
            return '<b>'+ this.x +'</b>: '+ Highcharts.numberFormat(this.y, 2) + 'Mt';
          }
        },
        plotOptions: {
          bar: {
            dataLabels: {
              enabled: false,
            },
          },
        },
        legend:{
          enabled:false
        },
        credits: {
          enabled: false,
        },
        series: [],
      },
    };
  },

  watch: {
    time: 'updateChart',
    'selectedCountry.selected':  'updateChart'
  },

  mounted() {
    this.loadInitialData();
  },

  methods: {

    loadInitialData(){
      const dateFormatted = this.formatDate(this.time);
      const dateData = this.data[dateFormatted];
      let power = 0;
      let gt = 0;
      let da = 0;
      let ind = 0;
      let res = 0;

      for (let country in dateData)
      {
        if (dateData[country]['Has Covid'] === true) // has to be changed to Has Carbon when the dataset is fixed
        {
          power += dateData[country]['Power'];
          gt += dateData[country]['Ground Transport'];
          da += dateData[country]['Domestic Aviation'];
          ind += dateData[country]['Industry'];
          res += dateData[country]['Residential'];
        }
      }

      if (this.chartOptions.series.length === 0)
      {
        this.chartOptions.series.push({
        name: '',
        data: [power, gt, ind, res, da],
      });
      }
      else
      {
        this.chartOptions.series[0].data = [power, gt, ind, res, da];
      }
    },

    updateChart(){

      const dateFormatted = this.formatDate(this.time);
      const dateData = this.data[dateFormatted];
      if (this.selectedCountry.selected !== 'country')
      {
        const countryData = dateData[this.selectedCountry.selected];
        this.chartOptions.series[0].data = [countryData['Power'], countryData['Ground Transport'], countryData['Industry'], countryData['Residential'], countryData['Domestic Aviation']];
        this.chartOptions.title.text = "CO2 emission per sector in " + this.selectedCountry.selected + ' ' + this.formatDate(this.time);
      }
      else {
        this.loadInitialData();
      }
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