<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Data</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>Data Upload</v-card-title>
      <v-card-text>
        <core-ImageUploader
          :multiple="true"
          @uploaded="$router.go()"
        />

      </v-card-text>
      <v-divider/>
      <v-card-title v-if="files.length !== 0">
        Images ({{files.length}}) of the project
      </v-card-title>
      <v-card-text v-if="files.length !== 0">
        <v-row justify="center" v-if="nPages > 1">
          <v-col cols="8">
            <v-container class="max-width">
              <v-pagination v-model="page" :length="nPages"
              ></v-pagination>
            </v-container>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col
            v-for="file in currentFiles"
            :key="file.id"
            class="col-6 col-lg-4 d-flex child-flex"
          >
            <core-FileInfo
              :file="file"
              @delete="deleteFile"
            />
          </v-col>

        </v-row>

        <v-row justify="center" v-if="nPages > 1">
          <v-col cols="8">
            <v-container class="max-width">
              <v-pagination v-model="page" :length="nPages"
              ></v-pagination>
            </v-container>
          </v-col>
        </v-row>

      </v-card-text>
    </v-card>



    <!-- Image deletion Dialog -->
    <v-dialog v-model="deleteDialog" width="600">
      <v-card>
        <core-LazyImage :file="fileToDelete" />
        <v-card-title class="grey lighten-2">
          Do you wish to delete file
          <span class="mx-1" v-if="fileToDelete !== undefined">
            <b>{{ fileToDelete.name }}</b>
          </span>?
        </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="deleteDialog = false">No</v-btn>
          <v-btn color="error" @click="deleteFileConfirmed">Yes</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- End Image deletion Dialog -->

  </v-container>
</template>

<script>
import DataService from '@/services/data.service';

export default {

  data() {
    return{
      files: [],
      page: 1,
      deleteDialog: false,
      fileToDelete: undefined,
    }
  },

  props: {
    elementsPerPage: {
      type: Number,
      default: 6
    },
  },

  computed: {
    projectId() {
      return this.$route.params.id;
    },

    nPages: function() {
      return Math.ceil(this.files.length / this.elementsPerPage)
    },

    currentFiles: function() {
      let start = (this.page - 1) * this.elementsPerPage;
      let end = this.page * this.elementsPerPage;

      return this.files.slice(start, end);
    }
  },


  created() {
    this.getFiles();
  },

  methods: {

    getFiles(){
      DataService.files.get(this.projectId)
        .then((files) => {
          this.files = files;
        })
    },

    deleteFile(file){
      this.deleteDialog = true;
      this.fileToDelete = file;
    },

    deleteFileConfirmed(){
      this.deleteDialog = false;
      DataService.files.delete(this.fileToDelete?.id);
      this.fileToDelete = undefined;
      this.$router.go(); // reload current view

    },
  }
};
</script>

<style scoped></style>
