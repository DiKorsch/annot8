<template>
  <div>


  <v-container fluid>

    <app-ViewHeader title="Image annotations">
      <core-ProjectSelector/>
    </app-ViewHeader>

    <v-card v-if="files.length != 0">
      <core-ImageAnnotator
        :file="selectedFile"
        @next="$refs.selector.next()"
        @previous="$refs.selector.previous()"
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
import { mapGetters } from 'vuex';

export default {
  name: "AnnotationsView",
  computed: {
    projectId() {
      return this.$route.params.id;
    },

    fileId() {
      return this.$route.params.fileId;
    },

    ...mapGetters({
      project: 'getCurrentProject',
      files: 'getProjectFiles',
    }),

    selectedFile() {
      if (this.selected === undefined && this.fileId === undefined)
        return this.files[0];
      return this.files.find(file => { return file.id == this.selected }) || this.files[0]
    }
  },

  data: () => ({
    selected: undefined,
  }),

  watch: {
    files: function(newVal) {
      if (newVal.length != 0)
        this.select(this.selectedFile)
    }
  },

  methods: {

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
    if (this.fileId != undefined)
      this.selected = Number(this.fileId);
  },

}
</script>
