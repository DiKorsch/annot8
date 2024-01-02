<template>
  <v-col
  offset=6 cols=6 justify="right"
  >
    <v-select
      outlined
      dense
      v-model="project"
      :items="projects"
      item-text="name"
      item-value="id"
      label="Selected project"
      prepend-inner-icon="mdi-book"
      append-icon="mdi-chevron-down-circle-outline"
    ></v-select>
  </v-col>
</template>

<script>
import { mapGetters } from 'vuex'
import DataService from '@/services/data.service';
import store from '@/store'

export default {
  name: "ProjectSelector",

  data: () => ({
    projects: [],
  }),

  computed: {

    ...mapGetters([
      'isProjectViewActive',
      'getCurrentProject',
    ]),

    project: {
      get: function() {
        return this.getCurrentProject
      },
      set: function(projectID){
        this.selectProject(projectID)
      }
    },
  },

  mounted: function() {
    DataService.project.get().then(
      (projects) => {
        this.projects = projects;
      });
  },

  methods: {

    selectProject(projectID){
      let project = this.projects.find((proj) => proj.id == projectID);
      console.log("[Project Selector] selected ", project)
      store.commit('setCurrentProject', project);

      this.$emit("selected", project);

      let route = this.$route;
      if (project === undefined || project.id == route.params.id)
        return;
      route.params.id = project.id;
      let {href} = this.$router.resolve(route);
      this.$router.push(href)
    }
  }
}
</script>
