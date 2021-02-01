<template>
  <b-row class="emission-chart">
      <highcharts class="hc" :options="chartOptions" ref="chart"></highcharts>
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
        title: {
          text: 'Emission Levels'
        },
        chart: {
          type: 'area',
          zoomType: 'x',
        },
        xAxis: {
          type: 'datetime',
          plotLines: []
        },
        yAxis: {
          title: {
            text: 'CO2 emissions (metric tons)'
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
          },

        },
        tooltip: {
          formatter: function() {
            return '<b>'+ this.series.name +'</b>: '+ Highcharts.numberFormat(this.y, 2) + 'Mt';
          }
        },
        series: []
      }
    }
  },

  mounted(){
   this.updateChart();
  },

  watch: {
    time: 'reloadChart',
    'settings.emissionSplit.selected':  'updateChart'
  },

  methods: {
    reloadChart(){
      this.chartOptions.xAxis.plotLines.pop();
      this.chartOptions.xAxis.plotLines.push({
          value: Date.parse(this.formatDate(this.time)),
          color: 'black',
          width: 2,
          id: 'first'
      })
    },

    updateChart(){
      while(this.chartOptions.series.length > 0)
        this.chartOptions.series.pop();
      if (this.settings.emissionSplit.selected === 'country')
      {
         //const randomData = [];
         for (let date in this.data){ //date will be the second param
           for (let country in this.data[date]) // country will be the name of the series
           {
             // check if a country has emission data
             if (this.data[date][country]['Has Covid'] === true && country !== 'World' ) // have to change to Has Carbon when the dataset is fixed
             {

               let count = 0;
               let index = 0;
               for (let i = 0; i < this.chartOptions.series.length; i++){
                  if (this.chartOptions.series[i].name === country)
                  {
                    count++;
                    index = i;
                  }
               }
               if (count >= 1)
               {
                 const emissions =  this.data[date][country]['Total Emissions'];
                 this.chartOptions.series[index].data.push([Date.parse(date), emissions ]);
               }
               else
               {
                 this.chartOptions.series.push({
                   name: country,
                   data: [[Date.parse(date), this.data[date][country]['Total Emissions']]]
                 });
               }
             }
           }
         }
      }
      else if (this.settings.emissionSplit.selected === 'sector') {

        const PowerData = [];
        const GroundTransportData = [];
        const DomesticAviationData = [];
        const IndustryData = [];
        const ResidentialData = [];
        for (let date in this.data) {
          //item - date, it will be the second param
          let power = 0;
          let gt = 0;
          let da = 0;
          let ind = 0;
          let res = 0;

          for (let country in this.data[date])
          {
            if (this.data[date][country]['Has Covid'] === true) // has to be changed to Has Carbon when the dataset is fixed
            // name of the series is the name of the array
            {
              power += this.data[date][country]['Power'];
              gt += this.data[date][country]['Ground Transport'];
              da += this.data[date][country]['Domestic Aviation'];
              ind += this.data[date][country]['Industry'];
              res += this.data[date][country]['Residential'];
            }
          }
          // add date + value to the correct sector array
          PowerData.push([Date.parse(date), power]);
          GroundTransportData.push([Date.parse(date), gt]);
          DomesticAviationData.push([Date.parse(date), da]);
          ResidentialData.push([Date.parse(date), res]);
          IndustryData.push([Date.parse(date), ind]);
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