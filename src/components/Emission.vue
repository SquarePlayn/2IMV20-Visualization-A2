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
            lineWidth: 0,
            marker: {
              lineWidth: 1,
              lineColor: '#666666'
            }
          }
        },
        series: []
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
      const date = this.formatDate(this.time);
      if (this.settings.emissionSplit.selected === 'country')
      {
         //const randomData = [];
         for (let date in this.data){ //date will be the second param
           for (let country in this.data[date]) // country will be the name of the series
           {
             // check if a country has emission data
             if (this.data[date][country]['Has Carbon'] === true)
             {
               // create a series for each country
               console.log(this.chartOptions.series.get(country));
             }



             /*const value = this.data[date][country]['Power'];
             const randomObject = [];
             randomObject.push(Date.parse(date), value);
           //  randomObject.push(value);
            // console.log(value);
             randomData.push(randomObject);*/
             //  console.log(this.data[item][x]['TotalEmission']); - dont have total emission yet
             //console.log(x['Emissions']);
           }
           //console.log(this.data[item]);
         }
         //this.chartOptions.series[0].name = 'try';
         //this.chartOptions.series[0].data = randomData;
       // console.log(this.chartOptions.series[0].data);
      }
      else if (this.settings.emissionSplit.selected === 'sector') {

        while(this.chartOptions.series.length > 0)
          this.chartOptions.series.pop();

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
            if (this.data[item][x]['Has Covid'] === true) // has to be changed to Has Carbon when the dataset is fixed
            //x - country
            // name of the series is the name of the array
            // need to sum sectors per country
            {
              power += this.data[item][x]['Power'];
              gt += this.data[item][x]['Ground Transport'];
              da += this.data[item][x]['Domestic Aviation'];
              ind += this.data[item][x]['Industry'];
              res += this.data[item][x]['Residential'];
            }
          }
          // add date + value to the correct sector array
          PowerData.push([Date.parse(item), power]);
          GroundTransportData.push([Date.parse(item), gt]);
          DomesticAviationData.push([Date.parse(item), da]);
          ResidentialData.push([Date.parse(item), res]);
          IndustryData.push([Date.parse(item), ind]);
        }

        this.chartOptions.series.push({
          name: 'Domestic Aviation',
          data: DomesticAviationData,
        });
        this.chartOptions.series.push({
          name: 'Residential',
          data: ResidentialData,
        });
        this.chartOptions.series.push({
          name: 'Ground Transport',
          data: GroundTransportData,
        });
        this.chartOptions.series.push({
          name: 'Industry',
          data: IndustryData,
        });
        this.chartOptions.series.push({
          name: 'Power',
          data: PowerData,
        });
      }
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