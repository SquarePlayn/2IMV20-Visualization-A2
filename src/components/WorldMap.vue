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

export default {
  name: "WorldMap",
  props: ['data', 'settings', 'time'],

  data() {
    return {
      countries: null,
      centers: null,
      selected: null,
      outline: {type: "Sphere"},
      projection: d3.geoMercator().scale(140).translate([1250 / 2, 460 / 1.4])
    };
  },

  computed: {
    width() {
      return 1250;
    },

    height() {
      // const [[x0, y0], [x1, y1]] = d3.geoPath(d3.geoMercator().fitWidth(this.width, this.outline)).bounds(this.outline);
      // const dy = Math.ceil(y1 - y0), l = Math.min(Math.ceil(x1 - x0), dy);
      // this.projection.scale(this.projection.scale() * (l - 1) / l).precision(0.2);
      // return dy;
      return 460;
    },

    // projection() {
    //   return ;
    // },
  },

  mounted() {
    this.loadCountries();
  },

  watch: {
    time: 'updateMap',
  },

  methods: {
    loadCountries() {
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
        .on('click', function(d) {
          // On clicking a country, give it the selected class and store it in the selected variable
          d3.select(this).classed('selected', true);
          if (that.selected) {
            d3.select(that.selected).classed('selected', false);
          }
          that.selected = this;
        })
        .on('mouseover', function(d) {
          // Detect hovering over
          d3.select(this).classed("hovered", true);
        })
        .on('mouseout', function(d) {
          // Reset hovered when moving mouse away
          d3.select(this).classed("hovered", false);
        })
      ;
    },

    createCenters() {
      //  https://developers.google.com/public-data/docs/canonical/countries_csv
      d3.select('#svg-centers')
        .selectAll('.country-center')
        .data(this.centers)
        .enter()
        .append('circle')
        .attr('r', 2)
        .attr('cx', (d) => {
          return this.projection([d.long, d.lat])[0];
        })
        .attr('cy', (d) => {
          return this.projection([d.long, d.lat])[1];
        });
    },

    updateMap() {
      // TODO
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

.selected {
  fill: yellow !important;
}

.hovered {
  fill: gray;
}
</style>