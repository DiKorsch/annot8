<template>
    <v-card
      @drop.prevent="onDrop($event)"
      @dragover.prevent="dragover = true"
      @dragenter.prevent="dragover = true"
      @dragleave.prevent="dragover = false"
      :class="{ 'grey lighten-2': dragover }"
    >
      <v-card-text>
        <input type="file" ref="file" style="display: none" v-on:change="onClick($event)">
        <v-row
          dense
          class="d-flex flex-column"
          align="center"
          justify="center"
          @click="$refs.file.click()"
          @mouseover="dragover = true"
          @mouseleave="dragover = false"

        >
          <v-icon :class="[dragover ? 'mt-2, mb-6' : 'mt-5']" size="60">
            mdi-cloud-upload
          </v-icon>
          <p>
            Drop your file(s) here, or click to select them.
          </p>
        </v-row>
        <v-virtual-scroll
          v-if="uploadedFiles.length > 0"
          :items="uploadedFiles"
          height="150"
          item-height="50"
        >
          <template v-slot:default="{ item }">
            <v-list-item :key="item.name">
              <v-list-item-content>
                <v-list-item-title>
                  <v-row>
                    <v-col cols=6>{{ item.name }}</v-col>
                    <v-col cols=6>
                      <span class="ml-3 text--secondary">
                        {{ prettyBytes(item.size) }}
                      </span>
                    </v-col>
                  </v-row>

                </v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn @click.stop="removeFile(item.name)" icon>
                  <v-icon> mdi-close-circle </v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>

            <v-divider></v-divider>
          </template>
        </v-virtual-scroll>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn plain @click.stop="submit">
          Upload
          <v-icon id="upload-button">mdi-upload</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
const prettyBytes = require('pretty-bytes');
import DataService from '@/services/data.service';

export default {
  name: "UploadComponent",
  props: {
    multiple: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dragover: false,
      uploadedFiles: [],
    };
  },

  computed: {
    projectId() {
      return this.$route.params.id;
    },
  },

  methods: {
    prettyBytes,

    removeFile(fileName) {
      // Find the index of the
      const index = this.uploadedFiles.findIndex(
        file => file.name === fileName
      );
      // If file is in uploaded files remove it
      if (index > -1) this.uploadedFiles.splice(index, 1);
    },

    onClick(e) {
      this.handleFiles(e.target.files);

    },

    onDrop(e) {
      this.handleFiles(e.dataTransfer.files);
    },

    handleFiles(files) {

      this.dragover = false;

      if (!this.multiple && files.length > 1){
        let message = "Only one file can be uploaded at a time";
        console.log(message)

      } else {
        for (const file of files) {
          this.uploadedFiles.push(file)
        }
      }
    },


    submit() {
      // If there aren't any files to be uploaded throw error
      if (!this.uploadedFiles.length > 0) {
        let message = "There are no files to upload";
        console.log(message)
      } else {
        // Send uploaded files to parent component
        // this.$emit("upload", );

        this.upload(this.uploadedFiles);
      }
    },

    upload(files) {
      for (const file of files){
        DataService.files.upload(
          this.projectId, file,
          this.uploadReady,
          this.progress
        )
      }
    },

    progress(file, event) {
      let percent = event.loaded / event.total * 100;
      console.log(`Upload Progress ${file.name}: ${percent}%`)
    },

    uploadReady(file, ok, content){
      if(!ok)
        return console.warn(file, content);

      let i = this.uploadedFiles.indexOf(file);

      if (i != -1)
        this.uploadedFiles.splice(i, 1)

      if (this.uploadedFiles.length == 0)
        this.$emit("uploaded")
    },
  }
};
</script>
