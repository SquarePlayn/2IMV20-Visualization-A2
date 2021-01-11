<template>
  <b-col cols="8" class="time-controls justify-content-center">
    <b-row>
      <b-input-group>
        <b-input-group-prepend>
          <b-button @click="previous">
            <b-icon-chevron-left/>
          </b-button>
          <b-button @click="togglePlay">
            <b-icon-pause v-if="playing"/>
            <b-icon-play v-else/>
          </b-button>
          <b-button @click="next">
            <b-icon-chevron-right/>
          </b-button>
        </b-input-group-prepend>
        <b-form-input
                id="time-slider"
                v-model="time"
                type="range"
                :min="min"
                :max="max"
                @input="pause"
        />
        <b-input-group-append is-text>
<!--          <b-input-group-text square>-->
            {{ time }}
<!--          </b-input-group-text>-->
        </b-input-group-append>
      </b-input-group>
    </b-row>
    <b-row>

    </b-row>
  </b-col>
</template>

<script>
export default {
  name: "TimeControls",

  props: ['value'],

  data() {
    return {
      time: 0,
      playing: false,
      timer: null,
      min: 0,
      max: 364,
    };
  },

  mounted() {
    this.time = this.value;
    this.timer = setInterval(() => this.advanceIfPlaying(), 500);
  },

  watch: {
    time: function(time) {
      this.$emit('input', this.time);
    },
  },

  methods: {
    /**
     * Toggle whether the time is playing/running
     */
    togglePlay() {
      this.playing = !this.playing;
    },

    pause() {
      this.playing = false;
    },

    /**
     * If the time is playing/running, advance time
     */
    advanceIfPlaying() {
      if (this.playing) {
        this.next();
        if (this.time >= this.max) {
          this.pause();
        }
      }
    },

    /**
     * Go forward in time 1 step
     */
    next() {
      if (this.time < this.max) {
        this.time++;
      }
    },

    /**
     * Go backwards in time 1 step
     */
    previous() {
      if (this.time > this.min) {
        this.time--;
      }
    },
  },
}
</script>

<style scoped>
.time-controls {
  background-color: gray;
}
</style>