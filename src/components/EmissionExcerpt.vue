<template>
  <b-row>
    <b-col class="emission-excerpt">
      Emission chart excerpt at current time will go here.
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "EmissionExcerpt",
  props: ['data', 'settings', 'time'],
}
</script>

<style scoped>
.emission-excerpt {
  background-color: deepskyblue;
  height: 48vh;
}
</style>