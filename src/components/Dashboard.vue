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
          <b-col cols="2" align-h="right">
            <selectors :settings="settings"/>
          </b-col>
          <b-col cols="8" align-h="center">
            <world-map :data="data" :settings="settings"/>
          </b-col>
          <b-col cols="2" align-h="left">
            <emission-excerpt :data="data" :settings="settings"/>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <time-controls v-model="time"/>
        </b-row>
        <b-row align-h="center">
          <emission :data="data" :settings="settings"/>
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

  data() {
    return {
      data: {
        emission: null,
        covid: null,
      },
      emissionLoaded: false,
      covidLoaded: false,

      time: 0,

      settings: {
        // Split emission on [sector, country]
        emissionSplit: {
          selected: 'sector',
          options: [
            { value: 'sector', text: "Sector" },
            { value: 'country', text: "Country" },
          ],
        },

        // Select covid numbers: [cases, recoveries, deaths]
        covidCount: {
          selected: 'cases',
          options: [
            { value: 'cases', text: 'Cases' },
            { value: 'recoveries', text: 'Recoveries' },
            { value: 'deaths', text: 'Deaths' },
          ],
        },

        // Select country (to display emission chart)
        // TODO
      },
    };
  },

  mounted() {
    this.loadData();
  },

  methods: {
    /**
     * Load the datasets
     */
    loadData() {
      // Async loading of emission data
      fetch("data/emission.json")
          .then(response => {
            this.data.emission = response.json();
            this.emissionLoaded = true;
          });
      // Async loading of covid data
      fetch("data/emission.json") // TODO Switch to covid.json once that's present
          .then(response => {
            this.data.covid = response.json();
            this.covidLoaded = true;
          });
    },
  },
};
</script>

<style scoped>

</style>