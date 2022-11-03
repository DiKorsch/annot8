<template>
  <v-container fluid>
    <v-row>
      <v-col class="col-8">
        <h1>Projects</h1>
      </v-col>
      <v-col class="col-4" align="right">
        <v-btn
          :to = "{ name: 'create_project' }"
          color="primary">
          Add Project
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-row dense>
        <core-ProjectInfo
          v-for="project in projects"
          :key="project.id"
          ref="projectInfos"
          :project="project"
          :cols="4"
          @selected="select"
        />
    </v-row>
  </v-container>

</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'ListView',

    computed: mapGetters('data', {
      projects: 'getProjects'
    }),

    data: () => ({
      selectedProject: undefined,
    }),

    created () {
      this.$store.dispatch('data/getProjects')
    },

    methods: {

      select(projectID) {
        this.selectedProject = projectID;
        let infos = this.$refs['projectInfos'];
        infos.forEach((info) => {
          info.selected = info.project.id === projectID;
        })
      }
    },
  }
</script>

<style scoped></style>
