import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'

import firebase from "firebase/app";
import "firebase/database";

const config = {
    apiKey: "AIzaSyD-pbgl5zLsJtNc4wg-9eLbIzuPsxZ-3wc",
    authDomain: "federatedlearning-2606.firebaseapp.com",
    databaseURL: "https://federatedlearning-2606-default-rtdb.firebaseio.com",
    projectId: "federatedlearning-2606",
    storageBucket: "federatedlearning-2606.appspot.com",
    messagingSenderId: "310165181800",
    appId: "1:310165181800:web:9819234baec4933caf72dd",
    measurementId: "G-BYNKPZ82GF"
};

firebase.initializeApp(config);

export const db = firebase.database();

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
