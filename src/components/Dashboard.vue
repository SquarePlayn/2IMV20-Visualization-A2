<template>
  <b-container
      fluid
      class="main-container h-100 d-flex flex-column"
  >
    <!-- Header -->
    <!-- (Disabled)
    <b-row>
      <app-header/>
    </b-row>
    -->
    <!-- Main content -->
    <b-row class="flex-grow-1">
      <b-spinner v-if="!dataLoaded"/>
      <b-col v-else>
        <b-row>
          <!-- Selectors -->
          <b-col cols="2" align-h="right">
            <selectors :settings="settings"/>
          </b-col>
          <!-- World Map -->
          <b-col cols="8" align-h="center">
            <world-map :data="data" :settings="settings" :time="time"/>
          </b-col>
          <!-- Emission Excerpt -->
          <b-col cols="2" align-h="left">
            <emission-excerpt :data="data" :settings="settings" :time="time"/>
          </b-col>
        </b-row>
        <!-- Time Controls -->
        <b-row align-h="center">
          <time-controls v-model="time"/>
        </b-row>
        <!-- Emission Graph -->
        <b-row align-h="center">
          <emission :data="data" :settings="settings" :time="time"/>
        </b-row>
      </b-col>
    </b-row>
    <!-- Footer -->
    <b-row>
      <app-footer/>
    </b-row>
  </b-container>
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
      data: null,
      dataLoaded: false,

      time: 0,

      settings: {
        // Split emission on [sector, country]
        emissionSplit: {
          label: 'Split emission on',
          selected: 'sector',
          options: [
            {value: 'sector', text: "Sector"},
            {value: 'country', text: "Country"},
          ],
        },

        // Select covid numbers: [cases, recoveries, deaths]
        covidCount: {
          label: 'Covid metric',
          selected: 'cases',
          options: [
            {value: 'cases', text: 'Cases'},
            {value: 'recoveries', text: 'Recoveries'},
            {value: 'deaths', text: 'Deaths'},
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
      // Async loading of the data
      axios.get("data/dataset.json")
        .then(response => {
          this.data = response.data;
          this.dataLoaded = true;
        });
    },
  },
};
</script>

<style scoped>
.main-container {
  background-color: whitesmoke;
}
</style>