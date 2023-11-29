<template>
  <v-container fluid v-if="project !== undefined">
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
      <v-card-title
        id="uploader-header"
        @click="localShowUploader = !localShowUploader"
        >
        Data Upload
        <v-spacer/>
        <v-icon v-if="showUploader">mdi-chevron-down</v-icon>
        <v-icon v-else>mdi-chevron-left</v-icon>
      </v-card-title>
      <v-card-text>
        <core-ImageUploader
          v-if="showUploader"
          :multiple="true"
          @uploaded="$router.go()"
        />

      </v-card-text>
      <v-divider/>
      <v-card-title v-if="files.length !== 0">
        Images {{this.start+1}} - {{this.end}} out of {{files.length}}
      </v-card-title>
      <v-card-text v-if="files.length !== 0">
        <core-CustomPaginator v-model="page" :length="nPages"/>
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
        <core-CustomPaginator v-model="page" :length="nPages"/>

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


    <utils-KeypressHandler @pressed="handleKeyPress($event)"/>
  </v-container>
</template>

<script>
import DataService from '@/services/data.service';
import { mapGetters } from 'vuex';

export default {

  data: () => ({
    page: 1,
    deleteDialog: false,
    fileToDelete: undefined,

    localShowUploader: false,
  }),

  props: {
    elementsPerPage: {
      type: Number,
      default: 6
    },
  },

  computed: {
    ...mapGetters({
      project: 'getCurrentProject',
      files: 'getProjectFiles',
    }),

    showUploader:{
      set(value){this.localShowUploader = value },
      get() {return this.files?.length===0 || this.localShowUploader}
    },

    projectId() {
      return this.project?.id;
    },

    nPages: function() {
      return Math.ceil((this.files?.length || 0) / this.elementsPerPage)
    },

    queryPage: function (){
      return Number(this.$route.query?.page) || 1;
    },

    start: function() {
      return (this.page - 1) * this.elementsPerPage;
    },

    end: function() {
      return Math.min(this.page * this.elementsPerPage, this.files.length);
    },

    currentFiles: function() {
      return this.files.slice(this.start, this.end);
    }
  },

  watch: {

    page: function(newVal){

      if (this.queryPage === newVal)
        return;

      this.$router.push({
        name: 'data',
        params: {id: this.projectId},
        query: {page: newVal}
      })
    }
  },

  methods: {

    handleKeyPress(event){
      switch (event.key){
        case "ArrowLeft":
          event.preventDefault();
          this.page = Math.max(1, this.page-1);
          break;
        case "ArrowRight":
          event.preventDefault();
          this.page = Math.min(this.nPages, this.page+1);
          break;
      }
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

<style scoped>
  #uploader-header {
    cursor: pointer;
  }
</style>
