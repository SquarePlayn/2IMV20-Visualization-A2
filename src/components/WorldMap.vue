<template>
  <b-row cols="8">
    <svg class="w-100 h-100 world-map">
      <circle class="test-circle" style="fill: #69b3a2" stroke="black" cx=200 cy=200 r=40></circle>
    </svg>
  </b-row>
</template>

<script>
import * as d3 from 'd3/dist/d3';

export default {
  name: "WorldMap",
  props: ['data', 'settings', 'time'],

  mounted() {
    this.setLine();
  },

  watch: {
    time: 'setLine',
  },

  methods: {
    setLine() {
      d3.select(".test-circle")  // select the elements that have the class 'test-circle'
          .style("stroke-width", this.time) // change their style: stroke width is now equal to pixels equal to time
    }
  }
}
</script>

<style scoped>
.world-map {
  min-height: 45vh;
  background-color: lightblue;
}
</style>