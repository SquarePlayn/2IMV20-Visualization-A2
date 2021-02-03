<template>
  <b-row>
    <svg class="w-100 h-100 world-map" id="world-map">
      <g id="svg-world"/>
      <g id="svg-centers"/>
      <g id="world-label"/>
    </svg>
  </b-row>
</template>

<script>
import * as d3 from 'd3/dist/d3';
import * as topojson from 'topojson/dist/topojson';
import { utility } from "../mixins/utility";
import _ from 'lodash';

export default {
  me: "WorldMap",
  props: ['data', 'settings', 'time', 'selectedCountry'],
  mixins: [utility],

  data() {
    return {
      // Data sets for country lines and centers
      countries: null,
      centers: null,

      // Currently selected country
      selected: null,
      hovered: null,

      // Geo coordinates to 2d coordinates projection
      projection: d3.geoMercator().scale(140).translate([1250 / 2, 460 / 1.4])
    };
  },

  computed: {
    dateData() {
      return this.data[this.formatDate(this.time)];
    },
  },

  mounted() {
    this.loadCountryDatasets();
  },

  watch: {
    time: 'updateMap',
    'settings.covidCount.selected': 'updateMap',
    selected: 'updateMap',
    hovered: 'updateMap',
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
      return this.getDateDataOfCountry(countryName)["Has Carbon"];
    },

    createWorld() {
      const g = d3.select('#svg-world');
      const path = d3.geoPath(this.projection);
      g.selectAll('.country')
        .data(this.countries)
        .enter()
        .append('path')
        .attr('class', 'country')
        .attr('d', path)
        .on('click', (event, d) => {
          // On clicking a country, give it the selected class and store it in the selected variable
          const name = this.convertCountryName(d.properties.name);
          if (this.isClickable(name)) { // But only if this is a clickable country
            if (this.selected === name) {
              // It was already selected, unselect it
              this.selectedCountry.selected = null;
              this.selected = null;
            } else {
              this.selected = name;
              // Select it
              this.selectedCountry.selected = this.selected;
            }
          }
        })
        .on('mouseover', (event, d) => {
          // Detect hovering over
          if (this.isClickable(d.properties.name)) {
            this.hovered = this.convertCountryName(d.properties.name);
          }
        })
        .on('mouseout', (event, d) => {
          if (this.isClickable(d.properties.name)) {
            // Reset hovered when moving mouse away
            this.hovered = null;
          }
        });

      // Make the map zoomable and pannable
      d3.select("#world-map")
        .call(d3.zoom().on("zoom", function (event) {
          d3.select('#svg-world').attr("transform", event.transform);
          d3.select('#svg-centers').attr("transform", event.transform);
          d3.select('#world-label').attr("transform", event.transform);
        }));

      // Set them to the right properties for the current time
      this.updateMap();
    },

    createCenters() {
      //  https://developers.google.com/public-data/docs/canonical/countries_csv

      // Filter out only countries that have center data
      const countryCoords = _.map(
        _.filter(
          this.dateData,
          country => this.isClickable(country["Country"])
        ), country => ({
          long: country["Country"] === 'World' ? -140 : country["Long"],
          lat: country["Country"] === 'World' ? -20 : country["Lat"],
          name: country["Country"],
        }));

      // Create the circles
      d3.select('#svg-centers')
        .selectAll('.country-center')
        .data(countryCoords)
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
        })
        .on('click', (event, d) => {
          const name = d.name;
          if (this.selected === name) {
            // It was already selected, unselect it
            this.selected = null;
            this.selectedCountry.selected = null;
          } else {
            // Select it
            this.selected = name;
            this.selectedCountry.selected = name;
          }
          this.updateMap();
        })
        .on('mouseover', (event, d) => {
          // Detect hovering over
          this.hovered = d.name;
        })
        .on('mouseout', (event, d) => {
          this.hovered = null;
        });

      // Create the label above the World circle
      const textLong = -140;
      const textLat = 15;
      d3.select('#world-label')
        .selectAll('.world-label')
        .data(["Other countries"])
        .enter()
        .append("svg:text")
        .text((d) => d)
        .attr('class', 'world-label')
        .attr('x', () => this.projection([textLong, textLat])[0])
        .attr('y', () => this.projection([textLong, textLat])[1])

      // Set them to the right properties for the current time
      this.updateMap();
    },

    getColumnFromMetric(metric) {
      const lookup = {
        'Confirmed': 'Confirmed Rolling Per Capita',
        'Recovered': 'Recovered Rolling Per Capita',
        'Deaths': 'Deaths Rolling Per Capita',
      };
      return lookup[metric];
    },

    updateMap() {
      // If there is no data for this date, don't do anything
      if (this.dateData === undefined) {
        console.log("Missing date: " + this.formatDate(this.time));
        return;
      }

      // Update the countries
      d3.select("#svg-world")
        .selectAll('path')
        .classed('selected', (d) => this.convertCountryName(d.properties.name) === this.selected)
        .classed('hovered', (d) => this.convertCountryName(d.properties.name) === this.hovered)
        .transition()
        .duration(10)
        .attr('fill', (d) => {
          const countryData = this.getDateDataOfCountry(d.properties.name);
          if (countryData === null) {
            return '#ffffff';
          }
          const metric = this.settings.covidCount.selected;
          const value = countryData[this.getColumnFromMetric(metric)];
          return this.getCountryColor(value, metric);
        });

      // Update the country circles
      d3.select('#svg-centers')
        .selectAll('circle')
        .classed('selected-center', (d) => d.name === this.selected)
        .classed('hovered', (d) => d.name === this.hovered)
        .transition()
        .duration(1)
        .attr('r', (d) => {
          // Size based on selected covid count
          const countryData = this.getDateDataOfCountry(d.name);
          const value = countryData['Total Emissions Rolling'];
          return Math.sqrt(value * 50);
        })
        .attr('fill', (d) => {
          // Color based on change
          const curr = this.getDateDataOfCountry(d.name)['Total Emissions Rolling'];
          const prev = this.getDateDataOfCountry(d.name)['Last Year Emissions Rolling'];
          const diff = curr - prev;
          const perc = diff / prev;
          return this.getEmissionCircleColor(perc);
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
  stroke: #333333;
  stroke-width: 0.5;
}

.country-center {
  stroke: #222222;
  stroke-width: 2;
}

.selected {
  stroke-width: 2;
  stroke: yellow !important;
}

.selected-center {
    stroke: yellow !important;
}

.hovered {
  fill: gray;
}

.world-label {
  text-anchor: middle;
  font-size: 20pt;
}
</style>