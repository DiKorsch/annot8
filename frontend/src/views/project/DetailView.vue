<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=8>
        <h1>Project Information</h1>
      </v-col>
      <v-col :cols=4 align="right">
        <v-btn :to = "{ name: 'projects' }" color="accent">
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
              <v-col v-if="isOwner" class="d-flex align-end flex-column">
                <v-btn
                  fab
                  color="error"
                  @click="proj_delete_dialog=true"
                >
                  <v-icon>mdi-trash-can-outline</v-icon>
                </v-btn>
                <v-dialog
                  v-model="proj_delete_dialog"
                  width="500"
                >
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

          <v-row>
            <v-col class="col-6">Description</v-col>
            <v-col class="col-6">{{ project.description }}</v-col>
          </v-row>

          <v-row>
            <v-col class="col-6">Owner</v-col>
            <v-col class="col-6">
              <v-row>

                <v-chip outlined cols=12>
                  <v-avatar left>
                    <v-icon>mdi-account-circle</v-icon>
                  </v-avatar>
                  <span v-if="isOwner">You</span>
                  <span v-else>{{ project.user }}</span>
                </v-chip>
              </v-row>
            </v-col>
          </v-row>

          <v-row>
            <v-col class="col-6">Collaborators</v-col>
            <v-col class="col-6"><core-ProjectCollaborators :project="project"/></v-col>
          </v-row>

          <v-row v-if="project.model">
            <v-col class="col-6">Model</v-col>
            <v-col class="col-6">{{ project.model }}</v-col>
          </v-row>

          <v-row v-if="project.label_provider">
            <v-col class="col-6">Label Provider</v-col>
            <v-col class="col-6">{{ project.label_provider }}</v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col class="col-6">Root Folder</v-col>
            <v-col class="col-6">{{ project.root_folder }}</v-col>
          </v-row>
          <v-row>
            <v-col class="col-6">Data Folder</v-col>
            <v-col class="col-6">{{ project.data_folder }}</v-col>
          </v-row>
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
  import { mapGetters } from 'vuex'
  import DataService from '@/services/data.service';

  export default {
    name: 'ShowProject',

    data (){
      return {
        proj_delete_dialog: false,
        project: null,
      }
    },

    computed: {

      ...mapGetters('auth', [
        'username',
      ]),

      isOwner(){
        return this.username == this.project.user;
      },

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
    }

  }
</script>

<style scoped></style>
