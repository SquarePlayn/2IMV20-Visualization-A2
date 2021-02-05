<template>
   <b-row>
      <highcharts class="emission-excerpt hc" :options="chartOptions" ref="chart" />
    </b-row>
</template>

<script>
import Highcharts from 'highcharts'
import stockInit from 'highcharts/modules/stock'
import { utility } from "../mixins/utility";

stockInit(Highcharts)

export default {
  name: "EmissionExcerpt",
  props: ['data', 'settings', 'time', 'selectedCountry'],
  mixins: [utility],
  data() {
    return {
      chartOptions: {
        chart: {
          type: "column",
          backgroundColor: 'whitesmoke',
        },
        title: {
          text: "CO2 emission per sector in<br/>the whole World<br/>at " + this.formatDate(this.time),
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
    'selectedCountry.selected':  'updateChart',
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
        if (dateData[country]['Has Carbon'] === true)
        {
          power += dateData[country]['Power'];
          gt += dateData[country]['Ground Transport'];
          da += dateData[country]['Domestic Aviation'];
          ind += dateData[country]['Industry'];
          res += dateData[country]['Residential'];
        }
      }
      console.log(dateData);

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
        this.chartOptions.title.text = "CO2 emission per sector in<br/>the whole World<br/>at " + this.formatDate(this.time);
      }
    },

    updateChart(){

      const dateFormatted = this.formatDate(this.time);
      const dateData = this.data[dateFormatted];
      if (this.selectedCountry.selected !== 'country' && this.selectedCountry.selected !== null)
      {
        const countryData = dateData[this.selectedCountry.selected];
        this.chartOptions.series[0].data = [countryData['Power'], countryData['Ground Transport'], countryData['Industry'], countryData['Residential'], countryData['Domestic Aviation']];
        if (this.selectedCountry.selected === 'World') this.chartOptions.title.text = 'CO2 emission per sector in<br/>other countries<br/> at' + this.formatDate(this.time)
        else this.chartOptions.title.text = 'CO2 emission per sector in<br/>' + this.selectedCountry.selected + '<br/>at ' + this.formatDate(this.time);
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
  width: 100%;
}
</style>