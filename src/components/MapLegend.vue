<template>
    <b-row class="map-legend justify-content-center p-3">
        <b-col cols="12">
            <template v-for="topic in TOPICS" v-if="topic.ifMetric === null || topic.ifMetric === covidMetric">
                <!-- Country color: covid metric per capita. 0, 0.0001, 0.0002 -->
                <b-row class="legend-header pt-2">
                    <h5>{{ topic.label }}</h5>
                </b-row>
                <b-row align-v="center" v-for="value in topic.values" :key="value.img">
                    <b-col cols="4">
                        <b-img class="legend-img" :src="'img/' + value.img"/>
                    </b-col>
                    <b-col class="legend-label">
                        {{ value.val }}
                    </b-col>
                </b-row>
            </template>
            <!-- Blob size: CO_2 Emission (metric ton): -->
        </b-col>
    </b-row>
</template>

<script>
  const TOPICS = [{
    label: 'Covid cases per capita',
    ifMetric: 'Confirmed',
    values: [{
      img: 'covid-high.png',
      val: '0.0002',
    }, {
      img: 'covid-high.png',
      val: '0.0001',
    },{
      img: 'covid-high.png',
      val: '0',
    },]
  }, {
    label: 'Covid recoveries per capita',
    ifMetric: 'Recovered',
    values: [{
      img: 'covid-high.png',
      val: '0.0002',
    }, {
      img: 'covid-high.png',
      val: '0.0001',
    },{
      img: 'covid-high.png',
      val: '0',
    },]
  }, {
    label: 'Covid deaths per capita',
    ifMetric: 'Deaths',
    values: [{
      img: 'covid-high.png',
      val: '0.0002',
    }, {
      img: 'covid-high.png',
      val: '0.0001',
    },{
      img: 'covid-high.png',
      val: '0',
    },]
  }, {
    label: 'CO2 emission (metric ton)',
    ifMetric: null,
    values: [{
      img: 'covid-high.png',
      val: '0.0002',
    }, {
      img: 'covid-high.png',
      val: '0.0001',
    },{
      img: 'covid-high.png',
      val: '0',
    },]
  }, {
    label: 'Difference in CO2 emission from 1 year earlier',
    ifMetric: null,
    values: [{
      img: 'covid-high.png',
      val: '0.0002',
    }, {
      img: 'covid-high.png',
      val: '0.0001',
    },{
      img: 'covid-high.png',
      val: '0',
    },]
  }];

  export default {
    name: "MapLegend",
    props: ['covidMetric'],
    data() {
      return {
        TOPICS: TOPICS,
      };
    },
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