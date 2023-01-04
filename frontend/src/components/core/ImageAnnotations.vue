<template>
  <div class="overlay"
    ref="overlay"
    :key="toggleBBoxUpdate"
    @click="mouseClicked"
    @mouseenter="mouseEnter"
    @mousemove="mouseMove"
    @mouseleave="mouseLeave"
  >
    <v-chip small label>{{ this.getDisplayLabel(this.fileLabel) }}</v-chip>
    <core-BoundingBox
      v-for="(box, i) in this.bboxes"
      :value="box"
      :key="i"
      :highlightId="typeof selectedBBox !== 'undefined' ? selectedBBox.id : undefined"
      @selectedBBox="$emit('selectedBBox', $event)"
    />

    <core-BoundingBox
      v-if="typeof currentBBox !== 'undefined'"
      :value="currentBBox"
    />
  </div>
</template>


<script>
import DataService from '@/services/data.service';

export default {
  name: "ImageAnnotations",

  props: {
    fileLabel: undefined,
    fileId: undefined,
    interaction: undefined,
    selectedBBox: undefined,
  },

  watch: {
    fileId: function() { // watch it
      this.getBBoxes();
    },
    interaction: function(oldInteraction, newInteraction) {
      if (oldInteraction === "draw_box" && newInteraction !== "draw_box") {
        this.x = null;
        this.y = null;
        this.currentBBox = undefined;
      }
    },
  },

  data: () => ({
    x: null,
    y: null,
    currentBBox: undefined,
    bboxes: [],
    toggleBBoxUpdate: false,
  }),

  created: function () {
    this.getBBoxes();
  },

  methods: {
    mouseEnter() {
      console.log('mouseenter');
      // this.$el.addEventListener('mousemove', this.mouseMove, false);
    },
    mouseLeave() {
      console.log('mouseleave');
      // this.$el.removeEventListener('mousemove', this.mouseMove());
    },
    mouseMove(event) {
      if (this.x !== null && this.y !== null && this.interaction === "draw-box") {
          this.currentBBox = this.calculateBBox(this.x, this.y, event.layerX, event.layerY);
      }
      // console.info(event.layerX, event.layerY);
    },
    mouseClicked(event) {
      if (this.interaction === "draw-box") {
        this.drawBBox(event);
      }
    },

    getDisplayLabel(label) {
      if (label !== null) {
        return label;
      } else {
        return "Unknown";
      }
    },

    generateBBoxes() {
      DataService.files.generate_bboxes(this.fileId)
        .then((ok) => {
          if (!ok){
            console.log("Failed to add generate bounding boxes.");
          }
          this.getBBoxes();
        });
    },
    drawBBox(event) {
      if (this.x !== null && this.y !== null) {
        this.add_bbox(this.x, this.y, event.layerX, event.layerY)
        this.resetDrawBBox();
      } else {
        this.x = event.layerX;
        this.y = event.layerY;
      }
    },
    resetDrawBBox() {
      this.x = null;
      this.y = null;
      this.currentBBox = undefined;
      console.log("Resetted draw_box")
    },

    calculateBBox(x1, y1, x2, y2) {
      if (x1 === null || y1 === null || x2 === null || y2 === null) {
        return undefined;
      }

      /*// Scale bounding box coordinates to [0,1].
      x1 = (x1 + 1) / this.$refs.overlay.clientWidth;
      x2 = (x2 + 1) / this.$refs.overlay.clientWidth;
      y1 = (y1 + 1) / this.$refs.overlay.clientHeight;
      y2 = (y2 + 1) / this.$refs.overlay.clientHeight;

      // Calculate width + height.
      this.width = Math.abs(x2 - x1);
      this.height = Math.abs(y2 - y1);

      // Switch x1 / x2 and y1 / y2 if necessary.
      if (x1 > x2) {
        x1 = x2;
      }
      if (y1 > y2) {
        y1 = y2;
      }

      return {
        x: x1,
        y: y1,
        width: this.width,
        height: this.height,
      }*/

      // Scale bounding box coordinates to [0,1].
      x1 = (x1 + 1) / this.$refs.overlay.clientWidth;
      x2 = (x2 + 1) / this.$refs.overlay.clientWidth;
      y1 = (y1 + 1) / this.$refs.overlay.clientHeight;
      y2 = (y2 + 1) / this.$refs.overlay.clientHeight;

      // Switch x1 / x2 and y1 / y2 if necessary.
      return {
        width: Math.abs(x2 - x1),
        height: Math.abs(y2 - y1),
        x: Math.min(x1, x2),
        y: Math.min(y1, y2),
      }
    },

    add_bbox(x1, y1, x2, y2, label) {
      // Add bounding box.
      // Label does not necessarily have to be set!
      DataService.files.add_bbox(this.fileId, this.currentBBox.x, this.currentBBox.y, this.currentBBox.width, this.currentBBox.height, label)
      // DataService.files.add_bbox(this.fileId, x1, y1, this.width, this.height, label)
        .then((ok) => {
          if (!ok){
            console.log("Failed to add bounding box.");
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
          this.getBBoxes();
        });
    },

    predictBBox(bbox) {
      DataService.bboxes.predict(bbox.id)
        .then((ok) => {
          if (!ok){
            console.log("Failed to predict bounding box.");
          }
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

    getBBoxes() {
      DataService.bboxes.get(this.fileId)
        .then((bboxes) => {
          this.bboxes = bboxes;
        });
      this.toggleBBoxUpdate=!this.toggleBBoxUpdates; // toggle to change key and trigger update
    },
  }

}
</script>

<style scoped>
  .overlay{
    /*background-color: rgba(255, 0, 0, 0.3);*/
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
