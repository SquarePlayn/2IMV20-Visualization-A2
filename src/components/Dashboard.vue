<template>
  <b-col
      style="height: 100vh; width: 100vw"
      class="bg-light"
  >
    <b-row>
      <app-header/>
    </b-row>
    <b-row>
      <!-- Main content -->
      <b-container fluid>
        <b-row>
          <b-col cols="2">
            <selectors/>
          </b-col>
          <b-col cols="8">
            <world-map/>
          </b-col>
          <b-col cols="2">
            <emission-excerpt/>
          </b-col>
        </b-row>
        <b-row>
          <time-controls/>
        </b-row>
        <b-row>
          <emission/>
        </b-row>
      </b-container>
    </b-row>
    <b-row class="justify-content-center">
      <app-footer/>
    </b-row>
  </b-col>
</template>

<script>
import Selectors from "@/components/Selectors";
import WorldMap from "@/components/WorldMap";
import EmissionExcerpt from "@/components/EmissionExcerpt";
import TimeControls from "@/components/TimeControls";
import Emission from "@/components/Emission";
import AppFooter from "@/components/AppFooter";
import AppHeader from "@/components/AppHeader";

export default {
  name: "Dashboard",
  components: {AppHeader, AppFooter, Emission, TimeControls, EmissionExcerpt, WorldMap, Selectors},
};
</script>

<style scoped>

</style>