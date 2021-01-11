<template>
  <b-row cols="8">
    <svg class="w-100 h-100 world-map">
      <g id="map"/>
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
      selected: null,
      outline: {type: "Sphere"},
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

    projection() {
      return d3.geoMercator().scale(140).translate([this.width / 2, this.height / 1.4]);
    },
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
    },

    createWorld() {
      const that = this;
      const g = d3.select('g');
      const path = d3.geoPath(this.projection);
      g.selectAll('path')
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