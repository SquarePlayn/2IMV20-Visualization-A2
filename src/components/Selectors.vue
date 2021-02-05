<template>
  <b-row class="selectors justify-content-center">
      <b-col cols="12">
        <!-- Form group for every setting -->
        <b-form-group
          class="setting"
          v-for="(setting, key) in settings"
          :key="key"
          :id="`selector-${key}`"
          :label="setting.label"
        >
          <!-- Use button style radio input -->
          <b-form-radio-group
            v-model="setting.selected"
            :options="setting.options"
            buttons
          />
        </b-form-group>
      </b-col>
  </b-row>
</template>

<script>
export default {
  name: "Selectors",
  props: ['settings'],
}
</script>

<style scoped>
.selectors {
  padding-top: 2em;
}

.setting {
  /* Spacing between settings */
  padding-bottom: 1em;
}
</style>