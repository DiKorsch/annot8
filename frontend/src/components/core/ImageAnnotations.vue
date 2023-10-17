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
      v-for="box in this.bboxes"
      :value="box"
      :key="box.id"
      :ref="`box-${box.id}`"
      @selectedBBox="$emit('selectedBBox', $event)"
    />

    <core-BoundingBox
      v-if="currentBBox !== undefined"
      :value="currentBBox"
    />

    <core-BoundingBox
      v-if="newBox !== undefined"
      v-model="newBox"
    />
  </div>
</template>


<script>

export default {
  name: "ImageAnnotations",

  props: {
    fileLabel: undefined,
    bboxes: undefined,
    interaction: undefined,
  },

  watch: {
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
    toggleBBoxUpdate: false,
    newBox: undefined,
  }),

  methods: {

    getCoordinates(event) {
      var bounds = event.currentTarget.getBoundingClientRect();
      var x = event.clientX - bounds.left;
      var y = event.clientY - bounds.top;
      return {x, y}
    },

    toggleSelect(boxId) {
      if (boxId !== undefined){
        let comp = this.$refs[`box-${boxId}`][0];
        let wasSelected = comp.selected;
        for (let _box of this.bboxes)
          this.$refs[`box-${_box.id}`][0].selected = false;
        comp.selected = !wasSelected;
        return comp.selected;
      }
    },

    highlight(boxId) {
      if (boxId !== undefined)
        this.$refs[`box-${boxId}`][0].highlight = true;
      else
        for (let _box of this.bboxes)
          this.$refs[`box-${_box.id}`][0].highlight = false;
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

    drawBBox(x, y) {

      if (this.x !== null && this.y !== null) {
        // second click
        this.$emit("addBBox", this.currentBBox)
        this.resetDrawBBox();
      } else {
        // first click
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
