<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Search Logo"
          class="shrink mr-2"
          contain
          src="https://img.icons8.com/external-wanicon-lineal-color-wanicon/64/000000/external-search-online-learning-wanicon-lineal-color-wanicon.png"
          transition="scale-transition"
          width="40"
        />
        <h2 class="font-weight-bold white--text">
          QTP Search
        </h2>
      </div>
    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
};
</script>
