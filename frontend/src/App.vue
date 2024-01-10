<template>
  <v-app id="annot8">
    <app-AppDrawer/>

    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>

    <app-GBIFExamples/>
    <app-SnackBar/>
  </v-app>
</template>

<script>
import DataService from '@/services/data.service';
import { mapGetters } from 'vuex'

export default {
  name: 'App',

  data: () => ({
      windowHeight: window.innerHeight
  }),

  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })

    if (!this.loggedIn)
      return

    DataService.initData()
  },

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },

  computed: {
    ...mapGetters("auth", ["loggedIn"])
  },

  methods: {
    onResize() {
      this.windowHeight = window.innerHeight;
    }
  }
};
</script>
