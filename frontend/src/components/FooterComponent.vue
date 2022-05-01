<template>

  <v-footer
    app
    padless
    fixed
    inset
  >

    <v-card
      flat
      tile
      class="indigo lighten-2 text-center flex"
    >
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

      <v-divider></v-divider>

      <v-card-text class="white--text pa-1">
        {{ new Date().getFullYear() }} — <strong>PyCS2</strong>
      </v-card-text>
    </v-card>

  </v-footer>
</template>

<script>

import { v4 as uuidv4 } from 'uuid';

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
  }
}
</script>
