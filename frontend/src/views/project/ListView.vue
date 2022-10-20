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
      <v-col
        v-for="project in projects"
        :key="project.id"
        :cols=4
      >
        <v-card
          outlined elevation="2"
          max-width=450px class="mx-auto"
          :to="{ name: 'project', params: { id: project.id }}"
          >
          <v-card-title>Name: {{project.name}}</v-card-title>
          <v-card-text>
              <p>Desc: {{project.description}}</p>
              <p>Root: {{project.root_folder}}</p>
          </v-card-text>
        </v-card>
      </v-col>
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

    created () {
      this.$store.dispatch('data/getProjects')
    },
  }
</script>

<style scoped></style>
