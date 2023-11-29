<template>
  <div >
    <utils-KeypressHandler
      @pressed="handleKeyPress($event)"/>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Crops</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>

    <v-card align="center" v-if="boxes.length != 0">
      <v-container>
        <core-CustomPaginator v-model="selectedTrack" :length="tracks.length"/>
        <h4 v-if="currentTrack !== undefined">{{ currentTrack.length }} Crops</h4>
        <v-row>
          <v-col
            v-for="(boxId, k) in currentTrack"
            :key="k"
            class="col-2 d-flex child-flex">
              <core-CroppedImage
                :file="file(boxId)"
                :box="box(boxId)"
                initialThumbSize="original"
                :qualitySelector="false"
              >
                <v-chip label small
                  :to="{
                    name: 'annotate',
                    params: {fileId: file(boxId).id},
                    query: {showInfo: boxId}}"
                  >
                  Go to {{file(boxId).name}}
                </v-chip>
              </core-CroppedImage>
          </v-col>
        </v-row>
        <core-CustomPaginator v-model="selectedTrack" :length="tracks.length"/>
      </v-container>
    </v-card>

    <v-alert
      v-else
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      No bounding boxes found in this project! Please <router-link :to="{name: 'annotate'}">annotate</router-link> some images!
    </v-alert>
  </v-container>


  </div>
</template>


<script>
import DataService from '@/services/data.service';

export default {
  name: "CropsView",
  computed: {
    projectId() {
      return this.$route.params.id;
    },

    currentTrack(){
      return this.tracks[this.selectedTrack-1];
    },

    // selectedFile() {
    //   if (this.selected === undefined && this.fileId === undefined)
    //     return this.files[0];
    //   return this.files.find(file => { return file.id == this.selected })
    // }
  },

  data: () => ({
    boxes: {},
    files: {},
    tracks: [],

    selectedTrack: 1,
  }),

  methods: {

    handleKeyPress(event){
      switch (event.key){
        case "ArrowLeft":
          event.preventDefault();
          this.selectedTrack = Math.max(1, this.selectedTrack-1);
          break;
        case "ArrowRight":
          event.preventDefault();
          this.selectedTrack = Math.min(this.tracks.length, this.selectedTrack+1);
          break;
      }
    },
    getCrops(){
      DataService.project.crops(this.projectId, true)
        .then((content) => {
          this.boxes = content.boxes;
          this.files = content.files;
          this.tracks = content.tracks;
        })
    },

    box(boxId){
      return this.boxes.get(boxId);
    },

    file(boxId){
      let box = this.box(boxId)
      return this.files.get(box.fileId);
    }
  },

  created() {
    this.getCrops();
  },

}
</script>
