<template>
  <div id="app">
    <dashboard/>
  </div>
</template>

<script>
import Dashboard from "@/components/Dashboard";

export default {
  name: 'App',
  components: {
    Dashboard,
  },
};
</script>

<!-- Global style -->
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}

html {
  height: 100%;
}

body {
  height: 100%;
}
</style>
