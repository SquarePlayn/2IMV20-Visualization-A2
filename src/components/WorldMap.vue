<template>
  <b-row>
    <svg class="w-100 h-100 world-map" id="world-map">
      <g id="svg-world"/>
      <g id="svg-centers"/>
    </svg>
  </b-row>
</template>

<script>
import * as d3 from 'd3/dist/d3';
import * as topojson from 'topojson/dist/topojson';
import { utility } from "../mixins/utility";
import _ from 'lodash';

export default {
  name: "WorldMap",
  props: ['data', 'settings', 'time'],
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
    dateData() {
      return this.data[this.formatDate(this.time)];
    }
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

    /**
     * Get the data of the selected day of a country
     * @param countryName
     * @return Object
     */
    getDateDataOfCountry(countryName) {
      countryName = this.convertCountryName(countryName);
      if (!(countryName in this.dateData)) {
        console.error("Missing data for country '" + countryName + "'.");
        return null;
      }
      return this.dateData[countryName];
    },

    /**
     * Check whether a country should be possible to be clicked / selected
     * @param countryName
     * @return boolean
     */
    isClickable(countryName) {
      // TODO Switch back to "Has Carbon" once dataset is fixed
      return this.getDateDataOfCountry(countryName)["Has Covid"];
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
        .on('click', function(event, d) {
          // On clicking a country, give it the selected class and store it in the selected variable
          const name = that.convertCountryName(d.properties.name);
          if (that.isClickable(name)) { // But only if this is a clickable country
            that.selected = name;
            that.updateMap();
          }
        })
        .on('mouseover', function(event, d) {
          // Detect hovering over
          if (that.isClickable(d.properties.name)) {
            d3.select(this).classed("hovered", true);
          }
        })
        .on('mouseout', function(event, d) {
          if (that.isClickable(d.properties.name)) {
            // Reset hovered when moving mouse away
            d3.select(this).classed("hovered", false);
          }
        });

      // Make the map zoomable and pannable
      d3.select("#world-map")
          .call(d3.zoom().on("zoom", function (event) {
            d3.select('#svg-world').attr("transform", event.transform);
            d3.select('#svg-centers').attr("transform", event.transform);
          }));
    },

    createCenters() {
      //  https://developers.google.com/public-data/docs/canonical/countries_csv

      console.log(this.dateData);
      // Filter out only countries that have center data
      const countryCoords = _.map(
        _.filter(
          this.dateData,
          country => this.isClickable(country["Country"])
        ), country => { return {
          long: country["Long"],
          lat: country["Lat"],
          name: country["Country"],
       };});

      console.log(countryCoords);

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
      // If there is no data for this date, don't do anything
      if (this.dateData === undefined) {
        console.log("Missing date: " + this.formatDate(this.time));
        return;
      }

      // Update the countries
      const that = this;
      d3.select("#svg-world")
        .selectAll('path')
        .classed('selected', function (d) {
          console.log("Checking selected of");
          console.log(d);
          return ;
        })
        .transition()
        .duration(1)
        .attr('fill', (d) => {
          const isSelected = that.convertCountryName(d.properties.name) === that.selected;
          if (isSelected) {
            return 'yellow';
          }

          return '#ffffff';
          const countryName = d.properties.name;
          const countryDataToday = dateData[countryName];
          const countryDataYesterday = yesterdayData[countryName];
          if (countryDataToday !== undefined && countryDataYesterday !== undefined) {
            // Color based on change
            const covidCountToday = countryDataToday[this.settings.covidCount.selected];
            const covidCountYesterday = countryDataYesterday[this.settings.covidCount.selected];

            const change = (covidCountToday - covidCountYesterday) / covidCountYesterday;

            const lower = -0.05;
            const upper = 0.05;

            const r = change < 0 ? 0 : 255 * (change / upper);
            const g = change > 0 ? 0 : 255 * (change / lower);
            const b = 0;
            const col = `rgb(${r}, ${g}, ${b})`;
            // console.log(`Setting ${countryName} to color ${col}`);
            // console.log(countryDataToday)
            // console.log(countryDataYesterday)
            return col;
          } else {
            return '#cccccc';
          }
        });

      return;

      // Update the country circles
      d3.select('#svg-centers')
        .selectAll('circle')
        .transition()
        .duration(1)
        .attr('r', (d) => {
          // Size based on selected covid count
          const countryData =  dateData[d.name];
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
  background-color: white;
  border: 1px solid gray;
}
</style>

<style>
.country {
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