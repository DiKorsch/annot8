<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Project Information</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="accent">
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
                  v-model="proj_delete_dialog"
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
                      <v-btn text @click="proj_delete_dialog=false">
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
                <v-list-item-title>Creator</v-list-item-title>
                <v-list-item-subtitle>{{ project.user }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Collaborators</v-list-item-title>

                <v-list-item-subtitle v-if="project.collaborators.length">
                  <ul>
                    <li v-for="(collaborator, index) in project.collaborators" :key="index">
                      {{ collaborator }}
                    </li>
                  </ul>
                </v-list-item-subtitle>
                <v-list-item-subtitle v-else>None</v-list-item-subtitle>

                <v-col :cols=3 >
                  <v-dialog
                    v-model="managed_collaborator_dialog"
                    width="500"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        block color="accent"
                        v-bind="attrs"
                        v-on="on"
                      >
                        Manage Collaborators
                      </v-btn>
                    </template>

                    <v-card>
                      <v-card-title class="text-h5 grey lighten-2">
                       Manage Collaborators
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                            Please enter the name of the user that you want to add or remove:

                            <v-text-field
                              label="Username"
                              v-model="managed_collaborator"
                              solo
                            ></v-text-field>

                            <span style="color:red">
                              {{ this.error_managed_collaborator }}
                            </span>
                        </v-container>
                      </v-card-text>

                      <v-divider></v-divider>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn @click="addCollaborator">
                          Add Collaborator
                        </v-btn>
                        <v-btn @click="removeCollaborator">
                          Remove Collaborator
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-col>
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
        proj_delete_dialog: false,
        managed_collaborator_dialog: false,
        project: null,
        managed_collaborator: '',
        error_managed_collaborator: '',
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
      },

      addCollaborator () {
        DataService.addCollaborator(this.projectId, this.managed_collaborator)
          .then((ok) => {
            if (ok){
              this.error_managed_collaborator="";
              this.$router.push({name: "projects"});
            } else {
              this.error_managed_collaborator="Collaborator could not be added. \
              Please check whether the username is spelled correctly. \
              Also, make sure that the user is not already a collaborator or \
              creator of the project!";
            }
          });
      },

      removeCollaborator () {
        DataService.removeCollaborator(this.projectId, this.managed_collaborator)
          .then((ok) => {
          if (ok){
            this.error_managed_collaborator="";
            this.$router.push({name: "projects"});
          } else {
            this.error_managed_collaborator="Collaborator could not be removed. \
            Please make sure that the username is spelled correctly!";
          }
        });
      }
    }

  }
</script>

<style scoped></style>
