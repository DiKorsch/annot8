<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=8>
        <h1>Project Settings</h1>
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
            <v-col cols="6">Description</v-col>
            <v-col cols="6">{{ project.description }}</v-col>
          </v-row>

          <v-row>
            <v-col cols="6">Owner</v-col>
            <v-col cols="6">
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
            <v-col cols="6">Collaborators</v-col>
            <v-col cols="6">
              <core-ProjectCollaborators :project="project"/>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>
          <!--<v-row>
            <v-col cols="6">Root Folder</v-col>
            <v-col cols="6">{{ project.rootFolder }}</v-col>
          </v-row> -->
          <v-row>
            <v-col cols="auto">Data Folder</v-col>
            <v-col cols="auto">
              <v-chip label small>{{ project.dataFolder }}</v-chip>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="3">Uploaded files:</v-col>
            <v-col cols="3"><v-chip>{{ project.stats.nFiles }}</v-chip></v-col>
            <v-col cols="3">Annotated boxes:</v-col>
            <v-col cols="3"><v-chip>{{ project.stats.nBoxes }}</v-chip></v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>
          <h4>Pipeline</h4>
          <v-row>
            <v-col cols="6">
              <v-select
                v-model="selectedDetector"
                :items="project.detectors"
                label="Detector"
                @change="selectDetector(selectedDetector)"

              ></v-select>
            </v-col>
            <v-col cols="6">
              <v-select
                v-model="selectedClassifier"
                :items="project.classifiers"
                label="Classifier"
                @change="selectClassifier(selectedClassifier)"
              ></v-select>
            </v-col>
          </v-row>
          <h4>Actions on all files</h4>

          <v-row align="center">
            <v-col cols="6">
              <v-btn color="teal lighten-2" block @click="runDetector">Run Detector</v-btn>
            </v-col>
            <v-col cols="6">
              <v-btn color="teal lighten-2" block>Run Classifier</v-btn>
            </v-col>
            <!-- <v-col cols="4">
              <v-btn color="teal lighten-2" block>Run Detector and classifier</v-btn>
            </v-col> -->
          </v-row>

          <v-row v-if="project.label_provider">
            <v-col cols="6">Label Provider</v-col>
            <v-col cols="6">{{ project.labelProvider }}</v-col>
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

    data: () => ({
      proj_delete_dialog: false,
      project: undefined,
      selectedClassifier: '',
      selectedDetector: '',
    }),

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
      DataService.project.get(this.projectId)
        .then((project) => {
          this.project = project;
          this.selectedClassifier = project.classifier
          this.selectedDetector = project.detector
        })
    },

    methods: {
      runDetector() {
        DataService.detector.run(this.projectId)
          .then((ok) => {
            if(!ok)
              console.error("COULD NOT RUN DETECTOR!")
          })
      },
      deleteProj () {
        DataService.project.delete(this.projectId)
          .then((ok) => {
            if (ok){
              this.$router.push({name: "projects"})
            }
          });
      },
      selectClassifier (classifier) {
        DataService.classifier.select(this.projectId, classifier)
          .then((ok) => {
            if (ok){
              this.$router.push({name: "project", params: { id: this.projectId}})
            }
          });
      },
      selectDetector (detector) {
        DataService.detector.select(this.projectId, detector)
          .then((ok) => {
            if (ok){
              this.$router.push({name: "project", params: { id: this.projectId}})
            }
          });
      },
    }

  }
</script>

<style scoped></style>
