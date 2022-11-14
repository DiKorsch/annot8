<template>
  <div>


  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Annotations</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>

    <v-card v-if="files.length != 0">
      <core-ImageAnnotator
        :file="selectedFile"
      />
      <v-footer :padless="true">

        <core-ImageSelector
          ref="selector"
          :images="files"
          :selectedImage="selected"
          @selected="select"
        />
      </v-footer>
    </v-card>

    <v-alert
      v-else
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      No files found in this project! Please <router-link :to="{name: 'data'}">upload</router-link> images for annotation!
    </v-alert>
  </v-container>


  </div>
</template>


<script>
import DataService from '@/services/data.service';

export default {
  computed: {
    projectId() {
      return this.$route.params.id;
    },

    fileId() {
      return this.$route.params.fileId;
    },

    selectedFile() {
      if (this.selected === undefined && this.fileId === undefined)
        return this.files[0];
      return this.files.find(file => { return file.id == this.selected })
    }
  },

  data: () => ({
    files: [],
    selected: undefined,
  }),

  methods: {

    getFiles(){
      DataService.files.get(this.projectId)
        .then((files) => {
          this.files = files;
          if (files.length != 0)
            this.select(this.selectedFile)
        })
    },

    select(image) {
      if (image === undefined){
        this.$router.push({
          name: 'annotations',
          params: {id: this.projectId},
        })
        this.selected = undefined;
        return
      }
      if (this.selected == image.id)
        return;
      this.selected = image.id;
      this.$router.replace({
        name: 'annotate',
        params: {id: this.projectId, fileId: image.id},
      })
    }
  },

  created() {
    this.getFiles();
    if (this.fileId != undefined)
      this.selected = Number(this.fileId);
  },

}
</script>
