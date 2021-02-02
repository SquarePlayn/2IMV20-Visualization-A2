<template>
    <b-row class="map-legend justify-content-center">
        <b-col cols="12">
            <!-- Country color: covid metric per capita. 0, 0.0001, 0.0002 -->
            <b-row class="legend-header">
                <h5>Covid {metric} per capita</h5>
            </b-row>
            <b-row align-v="center">
                <b-col cols="6">
                    <b-img class="legend-img" src="img/covid-high.png"/>
                </b-col>
                <b-col class="legend-label">
                    0.0002
                </b-col>
            </b-row>
            <!-- Blob size: CO_2 Emission (metric ton): -->
        </b-col>
    </b-row>
</template>

<script>
  export default {
    name: "MapLegend",
  }
</script>

<style scoped>
.map-legend {

}

.legend-header {
    justify-content: center;
    width: 100%;
}

.legend-label {
    width: 100%;
    height: 100%;
    text-align: left;
}

.legend-img {
    width: 100%;
}
</style>