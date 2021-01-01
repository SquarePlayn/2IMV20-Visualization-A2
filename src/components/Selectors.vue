<template>
  <b-row class="selectors">
    <b-col>
      <b-row
        v-for="(setting, key) in settings"
        :key="key"
      >
        <b-col align="right">
          <label :for="`selector-${key}`">
            (Something):
          </label>
        </b-col>
        <b-col>
          <b-form-select
            :id="`selector-${key}`"
            v-model="setting.selected"
            :options="setting.options"
          />
        </b-col>
      </b-row>
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
  background-color: deepskyblue;
}
</style>