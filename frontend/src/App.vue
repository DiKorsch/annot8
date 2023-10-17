<template>
  <v-app id="pycs2">
    <core-AppDrawer/>

    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>

    <core-AppFooter/>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data() {
    return {
      windowHeight: window.innerHeight
    }
  },

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
