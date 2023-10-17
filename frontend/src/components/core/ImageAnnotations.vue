<template>
  <div class="overlay"
    ref="overlay"
    :key="toggleBBoxUpdate"
    @click="mouseClicked"
    @mouseenter="mouseEnter"
    @mousemove="mouseMove"
    @mouseleave="mouseLeave"
  >
    <v-chip v-if="fileLabel" small label>
      {{ this.getDisplayLabel(this.fileLabel) }}
    </v-chip>
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

    <core-BoundingBox
      v-if="newBox !== undefined"
      v-model="newBox"
    />
  </div>
</template>


<script>
import DataService from '@/services/data.service';

class Box {


  constructor (x, y){
    this.x0 = x
    this.y0 = y

    this.x = x
    this.y = y
    this.w = 0
    this.h = 0
  }

  update(x, y){
    this.x = Math.min(this.x0, x)
    this.y = Math.min(this.y0, y)

    this.w = Math.max(this.x0, x) - this.x;
    this.h = Math.max(this.y0, y) - this.y;

    console.log(this.x, this.y, this.w, this.h)
  }
}

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
    minSize: 32,
    x: null,
    y: null,
    currentBBox: undefined,
    bboxes: [],
    toggleBBoxUpdate: false,
  }),

  created: function () {
    this.getBBoxes();
  },

  data: () => ({
    newBox: undefined,
  }),

  methods: {
    addBox: function(box){
      console.log()
      console.log(box.x, box.y, box.w, box.h)
    },

    getCoordinates(event) {
      var bounds = event.currentTarget.getBoundingClientRect();
      var x = event.clientX - bounds.left;
      var y = event.clientY - bounds.top;
      return {x, y}
    },

    mouseEnter() {
      console.debug('mouseenter');
      // this.$el.addEventListener('mousemove', this.mouseMove, false);
    },
    mouseLeave() {
      console.debug('mouseleave');
      // this.$el.removeEventListener('mousemove', this.mouseMove());
    },
    mouseMove(event) {
      var coords = this.getCoordinates(event);
      if (this.x !== null && this.y !== null && this.interaction === "draw-box") {
          this.currentBBox = this.calculateBBox(this.x, this.y, coords.x, coords.y);
      }

    },
    mouseClicked(event) {
      var coords = this.getCoordinates(event);

      if (this.interaction === "draw-box") {
        this.drawBBox(coords.x, coords.y);
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
    drawBBox(x, y) {

      if (this.x !== null && this.y !== null) {
        this.add_bbox(this.x, this.y, x, y)
        this.resetDrawBBox();
      } else {
        this.x = x;
        this.y = y;
      }
    },
    resetDrawBBox() {
      this.x = null;
      this.y = null;
      this.currentBBox = undefined;
      console.debug("Reset draw_box")
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
      var W = this.$refs.overlay.clientWidth
      var H = this.$refs.overlay.clientHeight
      x1 = (x1 + 1) / W;
      x2 = (x2 + 1) / W;
      y1 = (y1 + 1) / H;
      y2 = (y2 + 1) / H;

      // Switch x1 / x2 and y1 / y2 if necessary.
      return {
        width: Math.max(Math.abs(x2 - x1), this.minSize / W),
        height: Math.max(Math.abs(y2 - y1), this.minSize / H),
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
