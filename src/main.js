// Import Vue and other plugins
import Vue from 'vue';
import {BootstrapVue, IconsPlugin} from "bootstrap-vue";
import HighchartsVue from 'highcharts-vue';

// Import CSS
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

// Import components & store
import App from './App.vue';
import store from './store';

Vue.config.productionTip = false;

window.axios = require('axios').default;

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(HighchartsVue);

new Vue({
    store,
    render: h => h(App)
}).$mount('#app');
