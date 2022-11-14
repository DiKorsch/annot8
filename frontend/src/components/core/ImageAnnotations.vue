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
    />
  </div>
</template>


<script>
import DataService from '@/services/data.service';

export default {
  name: "ImageAnnotations",

  props: {
    fileLabel: undefined,
    fileId: undefined
  },

  watch: {
    fileId: function() { // watch it
      this.getBBoxes();
    }
  },

  data: () => ({
    x: null,
    y: null,
    width: null,
    height: null,
    bboxes: [],
    toggleBBoxUpdate: false,
  }),

  methods: {
    mouseEnter() {
      console.log('mouseenter');
      // this.$el.addEventListener('mousemove', this.mouseMove, false);
    },
    mouseLeave() {
      console.log('mouseleave');
      // this.$el.removeEventListener('mousemove', this.mouseMove());
    },
    //mouseMove(event) {
    //  console.info(event.layerX, event.layerY);
    //},
    mouseMove() {

    },
    mouseClicked(event) {
      if (this.x !== null && this.y !== null) {
        this.add_bbox(this.x, this.y, event.layerX, event.layerY, "Dummy label 2")
        this.x = null;
        this.y = null;
      } else {
        this.x = event.layerX;
        this.y = event.layerY;
      }
    },

    getDisplayLabel(label) {
      if (label !== null) {
        return label;
      } else {
        return "Unknown";
      }
    },

    add_bbox(x1, y1, x2, y2, label) {
      // Scale bounding box coordinates to [0,1].
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
        y1 = y2
      }

      // Add bounding box.
      // Label does not necessarily have to be set!
      DataService.files.add_bbox(this.fileId, x1, y1, this.width, this.height, label)
        .then((ok) => {
          if (!ok){
            console.log("Successfully added bounding box.");
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

    created() {
      this.getBBoxes();
    }
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
