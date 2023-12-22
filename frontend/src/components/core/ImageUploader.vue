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
          <v-icon :class="[dragover ? 'mt-2, mb-6' : 'mt-5']" size="48">
            mdi-cloud-upload
          </v-icon>
          <p>
            Drop your file(s) here, or click to select them.
          </p>
        </v-row>
        <v-virtual-scroll
          v-if="queuedFiles.length > 0"
          :items="queuedFiles"
          height="300"
          item-height="75"
        >
          <template v-slot:default="{ item }">
            <v-list-item :key="item.name">
              <v-list-item-content>
                <v-list-item-title>
                  <v-row>
                    <v-col cols="auto">{{ item.name }}</v-col>
                    <v-col cols="6">
                      <v-progress-linear
                        v-if="item.progress !== 0"
                        :value="item.progress"
                        height="25"
                        color="green"
                        background-color="green lighten-3"
                        rounded
                      >
                        <v-row dense class="text-center">
                          <v-col cols=6>{{item.loaded}} of {{item.size}} uploaded ({{ Math.ceil(item.progress) }}%) </v-col>
                          <v-col cols=6 v-if="item.rate !== undefined">{{item.rate}} ({{item.eta}})</v-col>
                        </v-row>
                      </v-progress-linear>
                    </v-col>
                    <v-col cols="3">
                      <v-alert
                        v-if="item.error !== undefined"
                        color="error"
                        icon="mdi-alert-circle-outline"
                        dense
                      >
                        {{item.error}}
                      </v-alert>
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
        <v-btn
          color="primary"
          @click.stop="submit"
          >
          Upload
          <v-icon id="upload-button">mdi-upload</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
</template>

<script>
const prettyBytes = require('pretty-bytes');
// import axios from 'axios'
import DataService from '@/services/data.service';
import File from "@/store/models/file"

class QueuedFile{
  constructor(file){
    this.name = file.name;
    this.size = prettyBytes(file.size)
    this.file = file;
    this.reset();
  }

  reset(){
    this.error = undefined;
    this.progress = 0;
    this.loaded = 0;

    this.rate = undefined;
    this.eta = undefined;
  }
}

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
      queuedFiles: [],

      state: undefined
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
      const index = this.queuedFiles.findIndex(
        file => file.name === fileName
      );
      // If file is in uploaded files remove it
      if (index > -1)
        this.queuedFiles.splice(index, 1);
    },

    onClick(e) {
      this.queueFiles(e.target.files);

    },

    onDrop(e) {
      this.queueFiles(e.dataTransfer.files);
    },

    queueFiles(files) {

      this.dragover = false;

      if (!this.multiple && files.length > 1)
        this.$store.dispatch("messages/error", {msg: "Only one file can be uploaded at a time"})
      else
        for (const file of files)
          this.queuedFiles.push(new QueuedFile(file))
    },


    submit() {
      // If there aren't any files to be uploaded throw error
      if (!this.queuedFiles.length > 0)
        return this.$store.dispatch("messages/error", {msg: "There are no files to upload"})

      this.state = "uploading"
      this.upload(this.queuedFiles);
    },

    async upload(files) {
      files.map((f) => f.reset());
      for (let file of files){
        await DataService.files.upload(
            this.projectId, file,
            this.uploadReady,
            this.progress
        )
      }
    },

    progress(queuedFile, event) {
      let percent = event.loaded / event.total * 100;
      let i = this.queuedFiles.indexOf(queuedFile);
      let f = this.queuedFiles[i];
      f.loaded = prettyBytes(event.loaded);
      f.progress = percent;
      if (event.rate !== undefined) {
        f.rate = `${prettyBytes(event.rate)}/s`;
        f.eta = `ETA: ${Math.round(Math.max(event.total - event.loaded, 0) / event.rate)} sec`;
      }

      // console.log(`[ImageUploader] Upload Progress ${file.name}: ${percent}%`)
    },

    uploadReady(queuedFile, ok, content){
      let i = this.queuedFiles.indexOf(queuedFile);
      if (i === -1)
        return console.error(`[ImageUploader] Upload file ${queuedFile.name} not found!`);

      if(!ok){
        this.queuedFiles[i].error = content.message;
        return console.warn(`[ImageUploader] Upload for file ${queuedFile.name} failed! Reason: ${content.message} | Code: ${content.code}`);
      }

      this.queuedFiles[i].ready = true;
      this.$emit("uploaded", new File(content.data))

      if (this.queuedFiles.every((f) => f.ready)){
        this.$store.dispatch("messages/info", {msg: "All files have been uploaded!"})
        this.$emit("ready")
        this.state = "ready";
        setTimeout(function(that){
          that.state = undefined;
          that.queuedFiles.splice(0, that.queuedFiles.length)
        }, 2000, this);

      }
    },
  },

  watch: {
    state: function(newValue, oldValue){
      if (oldValue === newValue)
        return

      if (newValue === "uploading")
        window.onbeforeunload = () => "Upload in progress";
        else
          window.onbeforeunload = null;
    }
  }
};
</script>
