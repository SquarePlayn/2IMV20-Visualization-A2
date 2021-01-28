<template>
  <b-row class="emission-chart">
    <div>
      <highcharts class="hc" :options="chartOptions" ref="chart"></highcharts>
    </div>
  </b-row>
</template>

<script>

import Highcharts from 'highcharts'
import { utility } from "../mixins/utility";

export default {
  name: "Emission",
  props: ['data', 'settings', 'time'],
  mixins: [utility],
  data() {
    return {
      chartOptions: {
        chart: {
          type: 'area',
          zoomType: 'x'
        },
        xAxis: {
          type: 'datetime'
        },
        yAxis: {
          title: {
            text: 'CO2 emissions'
          }
        },
        plotOptions: {
          area: {
            stacking: 'normal',
            lineColor: '#666666',
            lineWidth: 1,
            marker: {
              lineWidth: 1,
              lineColor: '#666666'
            }
          }
        },
        series: [{
          name: 'trial',
          data: [
            [
              1167609600000,
              0.7537
            ],
            [
              1167696000000,
              0.7537
            ],
            [
              1167782400000,
              0.7559
            ],
            [
              1167868800000,
              0.7631
            ],
            [
              1167955200000,
              0.7644
            ],
            [
              1579651200000,
              0.769
            ],]
        },
          ]
      }
    }
  },

  watch: {
    time: 'reloadChart',
    'settings.emissionSplit.selected':  'updateChart'
  },

  methods: {
    reloadChart(){
      //make the line move
    },

    updateChart(){

      console.log(this.chartOptions.series[0].data);
      const date = this.formatDate(this.time);
      //console.log(this.settings.emissionSplit.selected);
      if (this.settings.emissionSplit.selected === 'country')
      {
        const randomData = [];
        for (let item in this.data){
          //item - date, it will be the second param
          for (let x in this.data[item])
          {
            //x - country, it will be the name of the series
            const value = this.data[item][x]['Emissions']['Power'];
            const randomObject = [];
            randomObject.push(Date.parse(item), value);
          //  randomObject.push(value);
           // console.log(value);
            randomData.push(randomObject);
            //  console.log(this.data[item][x]['TotalEmission']); - dont have total emission yet
            //console.log(x['Emissions']);
          }
          //console.log(this.data[item]);
        }
        this.chartOptions.series[0].name = 'try';
        this.chartOptions.series[0].data = randomData;
        console.log(this.chartOptions.series[0].data);
      }
      else if (this.settings.emissionSplit.selected === 'sector') {
        const PowerData = [];
        const GroundTransportData = [];
        const DomesticAviationData = [];
        const IndustryData = [];
        const ResidentialData = [];
        for (let item in this.data) { //we iterate through each date
          //item - date, it will be the second param
          let power = 0;
          let gt = 0;
          let da = 0;
          let ind = 0;
          let res = 0;

          for (let x in this.data[item]) //we iterate through each country
          {
            //x - country
            // name of the series is the name of the array
            // need to sum sectors per country
            power += this.data[item][x]['Emissions']['Power'];
            gt += this.data[item][x]['Emissions']['Ground Transport'];
            da += this.data[item][x]['Emissions']['Domestic Aviation'];
            ind += this.data[item][x]['Emissions']['Industry'];
            res += this.data[item][x]['Emissions']['Residential'];
            //  const randomObject = [];
            //  randomObject.push(Date.parse(item), value);
            //  randomObject.push(value);
            // console.log(value);
            //   randomData.push(randomObject);
            //  console.log(this.data[item][x]['TotalEmission']); - dont have total emission yet
            //console.log(x['Emissions']);
          }
          // add date + value to the correct sector array
          PowerData.push([Date.parse(item), power]);
          GroundTransportData.push([Date.parse(item), gt]);
          DomesticAviationData.push([Date.parse(item), da]);
          ResidentialData.push([Date.parse(item), res]);
          IndustryData.push([Date.parse(item), ind]);
        }
        // assign series
        this.chartOptions.series[0].name = 'Power';
        this.chartOptions.series[0].data = PowerData;
        this.chartOptions.series.push({
          name: 'Industry',
          data: IndustryData,
        });
        this.chartOptions.series.push({
          name: 'Residential',
          data: ResidentialData,
        });
        this.chartOptions.series.push({
          name: 'Domestic Aviation',
          data: DomesticAviationData,
        });
        this.chartOptions.series.push({
          name: 'Ground Transport',
          data: GroundTransportData,
        });
      }
     /* const dateData = this.data[date];
      console.log(dateData['Emissions']);
      const emissions = dateData['Emissions'];
      this.chartOptions.series[0].data = [emissions['Power'], emissions['Ground Transport'], emissions['Industry'], emissions['Residential'], emissions['Domestic Aviation']];
      // this.chartOptions.series[0].data = [125,39, 78, 100, 89];
      console.log(this.settings.country.selected);
      console.log(this.selectedCountry.selected);*/
      //console.log(this.selectedCountry);
    },

  },
}
</script>

<style scoped>
.emission-chart {
  min-height: 45vh;
  background-color: antiquewhite;
}
</style>