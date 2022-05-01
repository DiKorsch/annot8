<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Project Information</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>
    <v-card outlined elevation="2" max-width=80% class="mx-auto">
      <div v-if="project != null">
        <v-card-title>
          <v-container fluid>
            <v-row>
              <v-col>{{ project.name }}</v-col>
              <v-col class="d-flex align-end flex-column">
                <v-dialog
                  v-model="dialog"
                  width="500"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      fab
                      color="error"
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>mdi-trash-can-outline</v-icon>
                    </v-btn>
                  </template>

                  <v-card>
                    <v-card-title class="text-h5 grey lighten-2">
                     Confirmation
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                          Do you really want to delete the project "{{ project.name }}"?
                      </v-container>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="red"
                        text
                        @click="deleteProj"
                      >
                        Yes, delete!
                      </v-btn>
                      <v-btn text @click="dialog=false">
                        No
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

              </v-col>
            </v-row>
          </v-container>
        </v-card-title>
        <v-card-text>

          <v-list two-line>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Description</v-list-item-title>
                <v-list-item-subtitle>{{ project.description }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Model</v-list-item-title>
                <v-list-item-subtitle>{{ project.model }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Label Provider</v-list-item-title>
                <v-list-item-subtitle>{{ project.label_provider }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Root Folder</v-list-item-title>
                <v-list-item-subtitle>{{ project.root_folder }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Data Folder</v-list-item-title>
                <v-list-item-subtitle>{{ project.data_folder }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
      </div>

      <div v-else>
        <v-card-title>
          Invalid Project!
        </v-card-title>
        <v-card-text>
          <v-container fluid>
            Please navigate back to your <router-link :to = "{ name: 'projects' }" >project list</router-link>.
          </v-container >
        </v-card-text>
      </div>
    </v-card>


  </v-container>
</template>

<script>
  // import { mapState } from 'vuex'
  import DataService from '@/services/data.service';

  export default {
    name: 'ShowProject',

    data (){
      return {
        dialog: false,
        project: null,
      }
    },

    computed: {

      // ...mapState(['data']),
      projectId() {
        return this.$route.params.id;
      },
    },

    created () {
      DataService.getProject(this.projectId)
        .then((project) => {
          this.project = project;
        })
    },

    methods: {
      deleteProj () {
        DataService.deleteProject(this.projectId)
          .then((ok) => {
            if (ok){
              this.$router.push({name: "projects"})
            }
          });
      }
    }

  }
</script>

<style scoped></style>
