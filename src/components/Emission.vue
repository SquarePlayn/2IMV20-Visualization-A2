<template>
  <b-row class="emission-chart">
    Emission chart will go here.
  </b-row>
</template>

<script>
export default {
  name: "Emission",
  props: ['data', 'settings', 'time'],
}
</script>

<style scoped>
.emission-chart {
  min-height: 45vh;
  background-color: antiquewhite;
}
</style>