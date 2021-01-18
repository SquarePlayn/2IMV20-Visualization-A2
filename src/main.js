// Import Vue and other plugins
import Vue from 'vue';
import {BootstrapVue, IconsPlugin} from "bootstrap-vue";

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

new Vue({
    store,
    render: h => h(App)
}).$mount('#app');
