<template>
  <div >
    <utils-KeypressHandler
      @pressed="handleKeyPress($event)"/>
  <v-container fluid>

    <app-ViewHeader title="Crop annotations">
      <core-ProjectSelector
        @selected="selectedTrack=1"
      />
    </app-ViewHeader>

    <v-alert
      v-if="tracks.length === 0"
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      <div v-if="cropsLoading">Loading crops...</div>
      <div v-else>
        No bounding boxes found in this project! Please <router-link :to="{name: 'annotate'}">annotate</router-link> some images!
      </div>
    </v-alert>
    <v-card align="center" v-else>

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

  </v-container>


  </div>
</template>


<script>
import { mapGetters } from 'vuex'

export default {
  name: "CropsView",
  computed: {
    projectId() {
      return this.$route.params.id;
    },

    currentTrack(){
      return this.tracks[this.selectedTrack-1];
    },

    ...mapGetters({
      crops: 'getProjectCrops',
      cropsLoading: 'isLoadingCrops',
    }),

    boxes() {
      return this.crops?.boxes || {};
    },

    files() {
      return this.crops?.files || {};
    },

    tracks() {
      return this.crops?.tracks || [];
    },
  },

  data: () => ({
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

    box(boxId){
      return this.boxes.get(boxId);
    },

    file(boxId){
      let box = this.box(boxId)
      return this.files.get(box.fileId);
    }
  },

}
</script>
