<template>
  <v-container fluid>
    <dialogs-TrackDelete
      :ids="cropsToRemove"
      @confirm="remove($event)"
      @close="cropsToRemove = []"
    />

    <dialogs-AnnotationDialog
      v-model="showAnnotationDialog"
      @selected="annotate({label: $event})"
    />

    <utils-KeypressHandler
      @pressed="handleKeyPress($event)"/>

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
    <v-row v-else>
      <v-col cols=10>
        <v-card align="center">

          <v-tabs v-model="tab">
            <v-tab>Grouped by Location</v-tab>
            <v-tab>Ungrouped</v-tab>
            <!-- <v-tab>...</v-tab> -->
          </v-tabs>


          <v-tabs-items v-model="tab">
            <v-tab-item>
              <v-container>
                <core-CustomPaginator v-model="selectedTrack" :length="tracks.length"/>
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
                            params: {fileId: (file(boxId) || {}).id},
                            query: {showInfo: boxId}}"
                          >
                          Go to {{(file(boxId) || {}).name}}
                        </v-chip>
                      </core-CroppedImage>
                  </v-col>
                </v-row>
                <core-CustomPaginator v-model="selectedTrack" :length="tracks.length"/>
              </v-container>

            </v-tab-item>
            <v-tab-item>
              <v-container>
                <v-row>
                  <v-col cols=10>
                    <core-CustomPaginator v-model="selectedUngrouped" :length="nUngroupedPages"/>
                  </v-col>
                  <v-col cols=2>
                    <v-chip># Crops per page: {{nUngroupedPerPage}}</v-chip>
                    <v-slider
                      v-model="nUngroupedPerPage"
                      min=6
                      max=48
                      step=6
                    ></v-slider>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col
                    v-for="(boxId, k) in currentUngroupedBoxes"
                    :key="k"
                    class="col-2 d-flex child-flex">
                      <v-badge
                        left
                        :value="selected.indexOf(boxId)!==-1"
                        icon="mdi-check">

                        <core-CroppedImage
                          :file="file(boxId)"
                          :box="box(boxId)"
                          initialThumbSize="original"
                          :qualitySelector="false"
                          @click="select(boxId)"
                        >
                          <v-chip label small
                            :to="{
                              name: 'annotate',
                              params: {fileId: (file(boxId) || {}).id},
                              query: {showInfo: boxId}}"
                            >
                            Go to {{(file(boxId) || {}).name}}
                          </v-chip>
                        </core-CroppedImage>
                      </v-badge>
                  </v-col>

                </v-row>
                <core-CustomPaginator v-model="selectedUngrouped" :length="nUngroupedPages"/>
              </v-container>
            </v-tab-item>

          </v-tabs-items>

        </v-card>
      </v-col>
      <v-col cols=2>

        <v-card v-if="tab == 0">
          <v-card-title>
            Edit track
          </v-card-title>

          <v-card-subtitle v-if="currentTrack !== undefined">
           Track with {{ currentTrack.length }} Crops
          </v-card-subtitle>
          <v-card-text v-if="currentTrackPredictions.length !== 0">
            Predicted as
            <v-btn
              v-for="(pred, i) in currentTrackPredictions" :key="i"
              @click="annotate({ids: currentTrack, label: pred[2]})"
              x-small
              :title="`Annotate the entire tracks as '${pred[2].name}'`">
              {{pred[0]}} ({{pred[1]}}x)
            </v-btn>
          </v-card-text>
          <v-card-text v-else>
            No predictions yet
          </v-card-text>
          <v-card-text v-if="currentTrackAnnotations.length !== 0">
            Annotated as
            <v-btn
              v-for="(annot, i) in currentTrackAnnotations" :key="i"
              @click="annotate({ids: currentTrack, label: annot[2]})"
              x-small
              :title="`Annotate the entire tracks as '${annot[2].name}'`">
              {{annot[0]}} ({{annot[1]}}x)
            </v-btn>
          </v-card-text>
          <v-card-text v-else>
            No annotations yet
          </v-card-text>
          <v-card-text>
            <v-row>
              <v-col cols=12>
                <v-btn @click="cropsToRemove = currentTrack"
                title="Delete entire track"
                block color="error"><v-icon left>mdi-trash-can-outline</v-icon> Delete</v-btn>
              </v-col>
              <v-col cols=12>
                <v-btn @click="cropsToAnnotate = currentTrack"

                title="Label entire track as ..."
                block><v-icon left>mdi-tag-outline</v-icon> Annotate</v-btn>
              </v-col>
              <v-col cols=12>
                <v-btn @click="classify(currentTrack)"
                title="Predict entire track"
                block><v-icon left>mdi-brain</v-icon> Classify</v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>


        <v-card v-if="tab == 1">
          <v-card-title>
            Edit selected
          </v-card-title>
          <v-card-subtitle v-if="selected.length !== 0">
            Selected {{selected.length}} crops <v-btn x-small @click="selected = []">reset</v-btn>
          </v-card-subtitle>
          <v-card-subtitle v-else>
            Select at least one crop
          </v-card-subtitle>

          <v-card-text>
            <v-row>
              <v-col cols=12>
                <v-btn @click="cropsToRemove = selected"
                :disabled="selected.length === 0" block color="error"><v-icon left>mdi-trash-can-outline</v-icon> Delete</v-btn>
              </v-col>
              <v-col cols=12>
                <v-btn @click="cropsToAnnotate = selected"
                :disabled="selected.length === 0" block><v-icon left>mdi-tag-outline</v-icon> Annotate</v-btn>
              </v-col>
              <v-col cols=12>
                <v-btn @click="classify(selected)"
                :disabled="selected.length === 0" block><v-icon left>mdi-brain</v-icon> Classify</v-btn>
              </v-col>
            </v-row>
          </v-card-text>

        </v-card>

      </v-col>
    </v-row>
  </v-container>
</template>


<script>
import { mapGetters } from 'vuex'
import DataService from '@/services/data.service';


export default {
  name: "CropsView",
  data: () => ({
    selectedTrack: 1,
    selectedUngrouped: 1,
    tab: 0,

    nUngroupedPerPage: 12,

    selected: [],

    cropsToRemove: [],
    cropsToAnnotate: [],
  }),

  computed: {

    ...mapGetters({
      crops: 'getProjectCrops',
      cropsLoading: 'isLoadingCrops',
    }),

    showAnnotationDialog: {
      get(){
        return this.cropsToAnnotate !== undefined && this.cropsToAnnotate.length !== 0
      },

      set() {
        this.cropsToAnnotate = []
      }
    },

    projectId() {
      return this.$route.params.id;
    },

    currentTrack(){
      return this.tracks[this.selectedTrack-1];
    },

    currentTrackPredictions(){
      const boxPreds = this.currentTrack.map((i) => this.box(i).predicted_label);
      const groupedPreds = Map.groupBy(boxPreds, (label) => label?.name);

      return Array.from(groupedPreds, ([key, preds]) => [key, preds.length, preds[0]]).filter((entry) => entry[0] !== undefined)
    },

    currentTrackAnnotations(){
      const boxPreds = this.currentTrack.map((i) => this.box(i).label);
      const groupedPreds = Map.groupBy(boxPreds, (label) => label?.name);

      return Array.from(groupedPreds, ([key, preds]) => [key, preds.length, preds[0]]).filter((entry) => entry[0] !== undefined)
    },

    currentUngrouped(){
      return this.ungroupedBoxes[this.selectedUngrouped-1];
    },

    boxes() {
      return this.crops?.boxes || {};
    },

    files() {
      return this.crops?.files || {};
    },

    tracks() {
      return this.crops?.tracks || [];
    },

    groupedBoxes (){
      return this.tracks.reduce((arr, track) => arr.concat(track), []);
    },

    ungroupedBoxes () {
      return Array.from(this.boxes).map((el)=>el[0])
        .filter((idx) => this.groupedBoxes.indexOf(idx) === -1)
    },

    nUngroupedPages(){

      return Math.ceil((this.ungroupedBoxes?.length || 0) / this.nUngroupedPerPage)
    },


    ungroupedStart: function() {
      return (this.selectedUngrouped - 1) * this.nUngroupedPerPage;
    },

    ungroupedEnd: function() {
      return Math.min(this.selectedUngrouped * this.nUngroupedPerPage, this.ungroupedBoxes.length);
    },

    currentUngroupedBoxes: function() {
      return this.ungroupedBoxes.slice(this.ungroupedStart, this.ungroupedEnd);
    },

  },

  watch: {
    crops: function(val, oldVal){
      console.log("Crops changed!", oldVal, val)
    }
  },

  methods: {

    handleKeyPress(event){
      switch (event.key){
        case "Delete":
          event.preventDefault();

          if(this.tab == 0)
            this.cropsToRemove = this.currentTrack;

          else if(this.tab == 1)
            this.cropsToRemove = this.selected;

          break;
        case "Enter":
          event.preventDefault();
          if (this.cropsToRemove !== undefined && this.cropsToRemove.length !== 0) {
            this.remove(this.cropsToRemove)
          }
          break;
        case "ArrowLeft":
          event.preventDefault();
          this.previous()
          break;
        case "ArrowRight":
          event.preventDefault();
          this.next()
          break;
      }
    },

    next(){
      if(this.tab == 0)
        this.selectedTrack = Math.min(this.tracks.length, this.selectedTrack+1);

      else if(this.tab == 1)
        this.selectedUngrouped = Math.min(this.nUngroupedPages, this.selectedUngrouped+1);

    },

    previous(){
      if(this.tab == 0)
        this.selectedTrack = Math.max(1, this.selectedTrack-1);

      else if(this.tab == 1)
        this.selectedUngrouped = Math.max(1, this.selectedUngrouped-1);


    },

    box(boxId){
      return this.boxes.get(boxId);
    },

    file(boxId){
      let box = this.box(boxId)
      if (box === undefined)
        return {}
      return this.files.get(box.fileId);
    },

    select(boxId){
      const index = this.selected.indexOf(boxId);
      if (index === -1)
        this.selected.push(boxId);
      else
        this.selected.splice(index, 1);
    },


    remove(ids){

      DataService.bboxes.deleteMany(ids)
        .then(({msg, idxs}) => {
          if (msg !== undefined)
            this.$store.dispatch("messages/info", {msg: msg})

          if(this.tab == 1)
            this.selected = []
          this.cropsToRemove = [];
          this.previous()
          for (const id of idxs)
            this.$store.commit("bboxDeleted", id)
        })
    },

    annotate({ids, label}){
      if (ids === undefined)
        if (this.tab == 0)
          ids = this.currentTrack

        else if (this.tab == 1)
          ids = this.selected


      if (ids === undefined || label === undefined){
        console.warn("[Crops] label or ids were not set!", ids, label)
        return
      }
      DataService.bboxes.setLabels(ids, label)
        .then(({msg, idxs}) => {
          if (idxs === undefined)
            this.$store.dispatch("messages/error", {msg: msg})

          else{
            this.$store.dispatch("messages/info", {msg: msg})

            for (const id of idxs)
              this.$store.commit("bboxLabelChanged", {id, label, pipeline: false})

          }
          this.cropsToAnnotate = []

          if(this.tab == 1)
            this.selected = []
        });

    },

    classify(ids){
      if (ids === undefined || ids.length === 0)
        this.$store.dispatch("messages/error",
          {msg: "No crops selected!"})

      DataService.bboxes.predictMany(ids)
        .then((task) => {
          if (task === undefined){
            console.error("[Image Annotator] Failed to predict bounding box.");
            return;
          }
          this.$store.commit("addTask", task);
        });
      console.log("Classify for", ids, "was clicked");

    },
  },

}
</script>
