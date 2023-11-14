<template>
  <v-navigation-drawer
    permanent
    app
  >
    <v-sheet
      color="grey lighten-4"
      class="pa-4"
    >

      <v-row class="align-center">
        <v-col class="d-flex flex-column col-3">
          <v-btn
            v-if="loggedIn"
            icon
            prominent
            x-large
            :to="{name: 'index'}"
          >
            <v-icon>mdi-account</v-icon>
          </v-btn>
          {{ username }}</v-col>
        <v-col class="d-flex justify-end col-9">
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
      <div
        v-for="link in getActiveLinks"
        :key="link.id"
      >
        <v-list-item
          :to="link.url(getCurrentProject)"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ link.text }}</v-list-item-title>
          </v-list-item-content>


        </v-list-item>

        <div v-if="!link.projectMenu && isProjectViewActive">

        <v-divider></v-divider>

        <v-list-item>
          <v-list-item-content>
            <v-chip outlined pill>
              <v-icon left>mdi-book</v-icon>
              {{ getCurrentProject.name }}
            </v-chip>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        </div>
      </div>
    </v-list>
    <app-AppFooter/>
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

  url(project){
    if (this.projectMenu){

        return {name: this.dest, params: {id: project.id}}

      }
      else
        return {name: this.dest}
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
      return this.links.filter(this.isActive);
    },

  },

  data: () => ({
    links: [
      new MenuItem(
        'My Projects',
        'mdi-book-multiple',
        'projects'),


      new MenuItem(
        'Data',
        'mdi-image-multiple-outline',
        'data',
        true
        ),

      new MenuItem(
        'Annotate images',
        'mdi-image-multiple',
        'annotations',
        true
        ),

      new MenuItem(
        'Show labels',
        'mdi-label-multiple',
        'labels',
        true
        ),

      new MenuItem(
        'Options',
        'mdi-cog',
        'project',
        true
        ),
    ],
  }),


  methods: {
    isActive(link) {
      return !link.projectMenu || (this.isProjectViewActive && link.projectMenu)
    }
  }

}

</script>

<style scoped>

</style>
