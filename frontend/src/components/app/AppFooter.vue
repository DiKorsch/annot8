<template>

  <v-footer
    padless
    fixed
  >

    <v-card
      flat
      tile
      class="primary text-center flex"
    >
      <v-card-text v-if="loggedIn">
        <core-TaskList/>
      </v-card-text>
      <v-divider/>

      <v-card-text class="pa-1">
        <v-btn
          v-for="item in icons"
          :key="item.id"
          :to="item.to"
          class="white--text"
          plain
        >
          {{ item.text }}
        </v-btn>
      </v-card-text>

      <v-divider/>

      <v-card-text class="white--text pa-1">
        {{ new Date().getFullYear() }} — <strong>Annot8</strong>
      </v-card-text>
    </v-card>
  </v-footer>
</template>

<script>

import { v4 as uuidv4 } from 'uuid';
import { mapGetters } from 'vuex'

class FooterItem {
  constructor(text, to, icon=""){
    this.id = uuidv4();
    this.text = text;
    this.to = to;
    this.icon = icon;
  }
}

export default {
  data () {
    return {
      icons: [
        new FooterItem('Impress', {name: 'impress'}),
        new FooterItem('About', {name: 'about'}),
      ],
    }
  },
  computed: {

    ...mapGetters('auth', [
      'loggedIn'
    ]),
  }
}
</script>
