<template>
  <b-row>
    <svg class="w-100 h-100 world-map">
      <g id="svg-world"/>
      <g id="svg-centers"/>
    </svg>
  </b-row>
</template>

<script>
import * as d3 from 'd3/dist/d3';
import * as topojson from 'topojson/dist/topojson';
import {utility} from "../mixins/utility";

export default {
  name: "WorldMap",
  props: ['data', 'settings', 'time', 'selectedCountry'],
  mixins: [utility],

  data() {
    return {
      // Data sets for country lines and centers
      countries: null,
      centers: null,

      // Currently selected country
      selected: null,

      // Geo coordinates to 2d coordinates projection
      projection: d3.geoMercator().scale(140).translate([1250 / 2, 460 / 1.4])
    };
  },

  computed: {
    width() {
      return 1250;
    },

    height() {
      return 460;
    },
  },

  mounted() {
    this.loadCountryDatasets();
  },

  watch: {
    time: 'updateMap',
    'settings.covidCount.selected': 'updateMap',
  },

  methods: {
    loadCountryDatasets() {
      // Async loading of the countries data
      axios.get('data/countries-110m.json')
          .then(response => {
            // Save the data
            const data = response.data;
            this.countries = topojson.feature(data, data.objects.countries).features;

            // Create the map
            this.createWorld();
          });

      axios.get('data/country-centers.json')
          .then(response => {
            //Save the data
            this.centers = response.data.countries;

            this.createCenters();
          })
    },

    createWorld() {
      const that = this;
      const g = d3.select('#svg-world');
      const path = d3.geoPath(this.projection);
      g.selectAll('.country')
          .data(this.countries)
          .enter()
          .append('path')
          .attr('class', 'country')
          .attr('d', path)
          .on('click', function (d) {
            // On clicking a country, give it the selected class and store it in the selected variable
            d3.select(this).classed('selected', true);
            that.settings.country.selected = d.target.__data__.properties.name;
            that.selectedCountry.selected = d.target.__data__.properties.name;
            // console.log(this.selectedCountryName);
            if (that.selected) {
              d3.select(that.selected).classed('selected', false);
            }
            that.selected = this;
          })
          .on('mouseover', function (d) {
            // Detect hovering over
            d3.select(this).classed("hovered", true);
          })
          .on('mouseout', function (d) {
            // Reset hovered when moving mouse away
            d3.select(this).classed("hovered", false);
          })
      ;
    },

    createCenters() {
      //  https://developers.google.com/public-data/docs/canonical/countries_csv

      // Create the circles
      d3.select('#svg-centers')
          .selectAll('.country-center')
          .data(this.centers)
          .enter()
          .append('circle')
          .attr('class', 'country-center')
          .attr('r', 0) // Filled at update
          .attr('fill', '#fff') // Filled at update
          .attr('cx', (d) => {
            return this.projection([d.long, d.lat])[0];
          })
          .attr('cy', (d) => {
            return this.projection([d.long, d.lat])[1];
          });

      // Set them to the right properties for the current time
      this.updateMap();
    },

    updateMap() {
      // Get the data of the selected day
      const dateFormatted = this.formatDate(this.time);
      const dateData = this.data[dateFormatted];

      // Get the data of yesterday, if possible
      const dateYesterday = this.formatDate(this.time - 1);
      const yesterdayData = this.data[dateYesterday];

      // If there is no data for this date, don't do anything
      if (dateData === undefined) {
        console.log("Missing date: " + dateFormatted);
        return;
      }
      if (yesterdayData === undefined) {
        // If yesterday is undefined, also don't do anything but no logging
        return;
      }

      // Update the country circles
      d3.select('#svg-centers')
          .selectAll('circle')
          .transition()
          .duration(1)
          .attr('r', (d) => {
            // Size based on selected covid count
            const countryData = dateData[d.name];
            const covidCount = countryData[this.settings.covidCount.selected];
            return Math.sqrt(covidCount) / 100.0;
          })
          .attr('fill', (d) => {
            // Color based on change
            const countryDataToday = dateData[d.name];
            const countryDataYesterday = yesterdayData[d.name];
            const covidCountToday = countryDataToday[this.settings.covidCount.selected];
            const covidCountYesterday = countryDataYesterday[this.settings.covidCount.selected];

            const change = (covidCountToday - covidCountYesterday) / covidCountYesterday;

            const lower = -0.05;
            const upper = 0.05;

            const r = change < 0 ? 0 : 255 * (change / upper);
            const g = change > 0 ? 0 : 255 * (change / lower);
            const b = 0;
            return `rgb(${r}, ${g}, ${b})`;
          });
    },
  }
}
</script>

<style scoped>
.world-map {
  min-height: 48vh;
  background-color: lightblue;
  border: 1px solid gray;
}
</style>

<style>
.country {
  fill: #cccccc;
  stroke: #333333;
  stroke-width: 0.5;
}

.country-center {
  stroke: #222222;
  stroke-width: 2;
}

.selected {
  fill: yellow !important;
}

.hovered {
  fill: gray;
}
</style>