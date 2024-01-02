<template>
  <v-container fluid>
    <app-ViewHeader
      title="Settings"
      icon="mdi-plus"
      dest="create_project"
      text="New Project"
    />

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
