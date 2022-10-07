<template>
  <v-navigation-drawer
    permanent
    app
  >
    <v-sheet
      color="grey lighten-4"
      class="pa-4"
    >
      <router-link :to="{ name: 'index' }">
      <v-avatar
        class="mb-4"
        color="grey darken-1"
        size="64"
      ></v-avatar>

      </router-link>
      <v-row>
        <v-col cols=6>{{ username }}</v-col>
        <v-col cols=3>
          <v-btn
            v-if="loggedIn"
            :to = "{ name: 'logout' }"
            color="primary"
            small
          >
            Logout <v-icon>mdi-logout</v-icon>
          </v-btn>
          <v-btn
            v-else
            :to = "{ name: 'login' }"
            color="primary"
            small
          >
            Login <v-icon>mdi-login</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-sheet>

    <v-divider></v-divider>

    <v-list v-if="loggedIn" >
      <v-list-item
        v-for="link in getActiveLinks"
        :key="link.id"
        :to="getLink(link)"
        link
      >
        <v-list-item-icon>
          <v-icon>{{ link.icon }}</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ link.text }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex'
import { v4 as uuidv4 } from 'uuid';

class MenuItem {
  constructor(text, icon, dest, projectMenu=false){
    this.id = uuidv4();
    this.text = text;
    this.icon = icon;
    this.dest = dest;
    this.projectMenu = projectMenu;
  }
}

export default {
  name: "DrawerComponent",

  computed: {

    ...mapGetters('auth', [
      'username',
      'loggedIn'
    ]),

    ...mapGetters([
      'isProjectViewActive',
      'getCurrentProject',

    ]),

    getActiveLinks () {
      return this.links.filter((item) => {
        return !item.projectMenu || (this.isProjectViewActive && item.projectMenu);
      });
    },

  },

  data: () => ({
    links: [
      new MenuItem(
        'My Projects',
        'mdi-book-multiple',
        'projects'),

      new MenuItem(
        'Project Info',
        'mdi-cog',
        'project',
        true
        ),

      new MenuItem(
        'Data',
        'mdi-image-multiple',
        'data',
        true
        ),

      new MenuItem(
        'Labels',
        'mdi-label-multiple',
        'labels',
        true
        ),

      new MenuItem(
        'Annotations',
        'mdi-account-hard-hat',
        'annotations',
        true
        ),
    ],
  }),


  methods: {
    getLink(link) {

      if (link.projectMenu){

        return {name: link.dest, params: {id: this.getCurrentProject}}

      }
      else
        return {name: link.dest}
    }
  }

}

</script>

<style scoped>

</style>
