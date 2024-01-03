<template>
  <v-app id="annot8">
    <app-AppDrawer/>

    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>

    <app-SnackBar/>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
      windowHeight: window.innerHeight
  }),

  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },

  methods: {
    onResize() {
      this.windowHeight = window.innerHeight;
    }
  }
};
</script>
