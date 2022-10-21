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
          @upload="upload"
        />

      </v-card-text>
      <v-divider/>
      <v-card-title>
        Data List
      </v-card-title>
      <v-card-text>
        <v-row dense>

          <v-col
            v-for="file in files"
            :key="file.id"
            class="col-6 col-lg-4 d-flex child-flex"
          >
            <core-FileInfo
              :file="file"
              @delete="deleteFile"
            />
          </v-col>

        </v-row>


      </v-card-text>
    </v-card>
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

  </v-container>
</template>

<script>
import DataService from '@/services/data.service';

export default {
  computed: {
    projectId() {
      return this.$route.params.id;
    },
  },

  data() {
    return{
      files: [],
      deleteDialog: false,
      fileToDelete: undefined,
    }
  },

  created() {
    this.getFiles();
  },

  methods: {
    upload(files){
      for (const file of files)
        DataService.files.upload(this.projectId, file)

      this.$router.go(); // reload current view
    },

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
