<template>
  <v-app id="pycs2">
    <Drawer/>

    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>

    <Footer/>
  </v-app>
</template>

<script>
import Drawer from "@/components/DrawerComponent"
import Footer from "@/components/FooterComponent"

export default {
  name: 'App',

  components: {
    Drawer,
    Footer,

  },

  data: () => ({
  }),
};
</script>
