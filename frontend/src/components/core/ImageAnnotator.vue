<template>
    <div align="center">
      <v-row>
        <v-col cols="auto">
          <core-ImageAnnotatorOptionBar
            @action="setInteraction($event)"
            @showInfo="showInfo=!showInfo"
          />
        </v-col>

        <v-col>

          <core-LazyImage
            :file="file"
            thumbSize="large"
            :maxHeight="maxHeight"
          >

            <core-ImageAnnotations
              ref="imageAnnotations"
              :interaction="interaction"
              :fileLabel="file.label"
              :bboxes="bboxes"
              @addBBox="addBBox($event)"
              @selectedBBox="bboxClicked($event)"
            />
          </core-LazyImage>
        </v-col>

        <v-col cols="3">
          <core-InfoBox v-if="showInfo"
            ref="infoBox"
            :selectedBBox="selectedBBox"
            :bboxes="bboxes"
            :file="file"
            :maxHeight="maxHeight"
            @highlight="$refs.imageAnnotations.highlight($event)"
            @toggle="toggle($event)"
            @select="select($event)"
            @remove="removeBBox($event)"
          />
        </v-col>
      </v-row>
    </div>
</template>

<script>

import DataService from '@/services/data.service';

export default {
  name: "ImageAnnotator",

  props: {
    file: undefined,
    maxHeight: {
      type: Number,
      default: () => 675
    },
  },

  data: () => ({
    interaction: 'select',
    selectedBBox: undefined,

    showInfo: false,
    bboxes: [],
  }),

  created: function () {
    this.getBBoxes();
  },

  watch: {
    file: function(){
      this.getBBoxes();
      this.selectedBBox = undefined;
    }
  },

  computed: {
    fileId: function() {
      return this.file.id;
    },

  },


  methods: {

    setInteraction(interaction) {
      this.interaction = interaction;

      console.log("new interaction:", interaction)
      if (interaction === "add"){
        // unselect the bbox if it is set
        this.select(this.selectedBBox);
      }
      // if (!(interaction === "info-box" || interaction === "label-box" || interaction === "confirm-box") && this.selectedBBox !== undefined) {
      //   this.selectedBBox = undefined;
      // }
      if (interaction === "detect") {
        this.estimateBBoxes();
      }
    },
    resetInteraction() {
      if (this.interaction === "draw-box") {
        this.$refs.imageAnnotations.resetDrawBBox();
      }
    },

    addBBox(bbox, label) {
      // Add bounding box.
      // Label does not necessarily have to be set!
      DataService.files.add_bbox(this.fileId, bbox.x, bbox.y, bbox.width, bbox.height, label)
        .then((ok) => {
          if (!ok){
            console.log("Failed to add bounding box.");
          }
          this.$emit('updateBboxes');
          this.getBBoxes();
        });
    },

    estimateBBoxes() {
      DataService.files.generate_bboxes(this.fileId)
        .then((ok) => {
          if (!ok){
            console.log("Failed to add generate bounding boxes.");
          }
          this.getBBoxes();
        });
    },

    labelBBox(bbox, label) {
      DataService.bboxes.set_label(bbox.id, label)
        .then((ok) => {
          if (!ok){
            console.log("Failed to label bounding box.");
          }
          this.emit('updateBboxes');
          this.getBBoxes();
        });
    },

    predictBBox(bbox) {
      DataService.bboxes.predict(bbox.id)
        .then((ok) => {
          if (!ok){
            console.log("Failed to predict bounding box.");
          }
          this.emit('updateBboxes');
          this.getBBoxes();
        });
    },

    removeBBox(bbox) {
      DataService.bboxes.delete(bbox.id)
        .then((ok) => {
          if (!ok){
            console.log("Failed to remove bounding box.");
          }
          this.getBBoxes();
        });
    },

    confirmBBox(bbox) {
      if (bbox.annotationId === null) {
        console.log("Cannot confirm bbox annotation because the given bbox has no annotation.")
        return false;
      }

      DataService.confirmator.toggle(bbox.annotationId)
        .then((ok) => {
          if (!ok){
            console.log("Failed to change confirmation status of bounding box.");
          }
          this.getBBoxes();
        });
    },

    toggle(bbox){
      let hidden = this.$refs.imageAnnotations.toggleVisibility(bbox?.id)
      this.$refs.infoBox.markHidden(bbox?.id, hidden)
    },

    select(bbox){
      if(this.$refs.imageAnnotations.toggleSelect(bbox?.id))
        this.selectedBBox = bbox;
      else
        this.selectedBBox = undefined;
    },

    getBBoxes() {
      DataService.bboxes.get(this.fileId)
        .then((bboxes) => {
          this.bboxes = bboxes;
        });
      // this.toggleBBoxUpdate=!this.toggleBBoxUpdates; // toggle to change key and trigger update
    },

    bboxClicked(bbox) {
      console.log("Clicked on", bbox?.id, this.interaction)

      // // Manage corresponding interactions.
      if (bbox === undefined || this.interaction === "add")
        return;
      this.select(bbox);
      // } else if (this.interaction === "select" || this.interaction === "edit") {
      // } else if (this.interaction === "remove-box") {
      //   this.removeBBox(bbox);
      // } else if (this.interaction === "label-box") {
      //   this.labelBBox(this.selectedBBox, "Dummy label 2");
      // } else if (this.interaction === "predict-box") {
      //   this.predictBBox(this.selectedBBox);
      // } else if (this.interaction === "confirm-box") {
      //   this.confirmBBox(this.selectedBBox);

    }
  }
}
</script>
