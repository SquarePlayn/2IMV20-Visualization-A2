<template>
    <b-row class="map-legend justify-content-center p-3">
        <b-col cols="12">
            <template v-for="topic in TOPICS" v-if="topic.ifMetric === null || topic.ifMetric === covidMetric">
                <!-- Country color: covid metric per capita. 0, 0.0001, 0.0002 -->
                <b-row class="legend-header pt-2" no-gutters>
                    <b-col>
                        <h5>{{ topic.label }}</h5>
                        <span class="text-muted">{{  topic.subtitle }}</span>
                    </b-col>
                </b-row>
                <b-row align-v="center" v-for="value in topic.values" :key="value.img" class="p-1">
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
    label: 'Covid cases',
    subtitle: 'Per 100.000 people per day',
    ifMetric: 'Confirmed',
    values: [{
      img: 'cases-high.png',
      val: '20',
    }, {
      img: 'cases-middle.png',
      val: '10',
    },{
      img: 'covid-0.png',
      val: '0',
    },]
  }, {
    label: 'Covid recoveries',
    subtitle: 'Per 100.000 people per day',
    ifMetric: 'Recovered',
    values: [{
      img: 'recovered-high.png',
      val: '1',
    }, {
      img: 'recovered-middle.png',
      val: '0.5',
    },{
      img: 'covid-0.png',
      val: '0',
    },]
  }, {
    label: 'Covid deaths',
    subtitle: 'Per 100.000 people per day',
    ifMetric: 'Deaths',
    values: [{
      img: 'deaths-high.png',
      val: '0.8',
    }, {
      img: 'deaths-middle.png',
      val: '0.4',
    },{
      img: 'covid-0.png',
      val: '0',
    },]
  }, {
    label: 'CO2 emission',
    subtitle: 'Metric ton per day',
    ifMetric: null,
    values: [{
      img: 'emission-high.png',
      val: '12',
    }, {
      img: 'emission-middle.png',
      val: '2',
    },{
      img: 'emission-low.png',
      val: '0.5',
    },]
  }, {
    label: 'Difference in CO2 emission',
    subtitle: 'Compared to the same day last year',
    ifMetric: null,
    values: [{
      img: 'diff-best.png',
      val: '> +24%',
    }, {
      img: 'diff-good.png',
      val: '+8% to +24%',
    },{
      img: 'diff-neutral.png',
      val: '-8% to +8%',
    },{
      img: 'diff-bad.png',
      val: '-8% to -24%',
    },{
      img: 'diff-worst.png',
      val: '< -24%',
    }]
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