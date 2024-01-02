<template>
  <v-container fluid v-if="project !== undefined">
    <dialogs-ImageDelete
      :file="fileToDelete"
      @close="fileToDelete = undefined"
      @confirm="confirmFileDelete($event)"
    />

    <app-ViewHeader title="Data">
      <core-ProjectSelector
        @selected="page=1"
      />
    </app-ViewHeader>
    <v-card
      @dragover.prevent="localShowUploader = true"
      @dragenter.prevent="localShowUploader = true"
    >
      <v-card-title
        class="clickable"
        @click="localShowUploader = !localShowUploader"
        >
        Data Upload
        <v-spacer/>
        <v-icon v-if="showUploader">mdi-chevron-down</v-icon>
        <v-icon v-else>mdi-chevron-left</v-icon>
      </v-card-title>
      <v-card-text>
        <core-ImageUploader
          :class="{hidden: !showUploader}"
          :multiple="true"
          @uploaded="$store.commit('fileUploaded', $event)"
        />

      </v-card-text>
      <v-divider/>
      <v-card-title
        class="clickable"
        v-if="files.length !== 0"
        @click="showData = !showData"
      >
        Images {{this.start+1}} - {{this.end}} out of {{files.length}}
        <v-spacer/>
        <v-icon v-if="showData">mdi-chevron-down</v-icon>
        <v-icon v-else>mdi-chevron-left</v-icon>
      </v-card-title>
      <v-card-text v-if="showData && files.length !== 0">
        <core-CustomPaginator v-model="page" :length="nPages"/>
        <v-row dense>
          <v-col
            v-for="file in currentFiles"
            :key="file.id"
            class="col-auto col-lg-3 d-flex child-flex"
          >
            <core-FileInfo
              :file="file"
              @delete="fileToDelete = file"
            />
          </v-col>

        </v-row>
        <core-CustomPaginator v-model="page" :length="nPages"/>

      </v-card-text>
    </v-card>

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
    showData: true,
  }),

  props: {
    elementsPerPage: {
      type: Number,
      default: 8
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

      console.log("Going to new page", newVal)
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

    confirmFileDelete(file){
      DataService.files.delete(file?.id)
        .then((ok) => {
          if(!ok)
            this.$store.dispatch("messages/error",
              {msg: `Could not delete ${file.name}!`})
          else
            this.$store.commit("fileDeleted", file)
        });
      this.fileToDelete = undefined;
    },
  }
};
</script>

<style scoped>
  .clickable {
    cursor: pointer;
  }

  .hidden {
    display: none;
  }
</style>
