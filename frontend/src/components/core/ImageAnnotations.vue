<template>
  <div class="overlay"
    ref="overlay"
    :key="toggleBBoxUpdate"
    @click.prevent="mouseClicked"
    @mouseenter="mouseEnter"
    @mousemove="mouseMove"
    @mouseleave="mouseLeave"

    @contextmenu="rightClick"
  >
    <v-chip v-if="fileLabel" small label>
      {{ this.getDisplayLabel(this.fileLabel) }}
    </v-chip>
    <core-BoundingBox
      v-for="box in this.bboxes"
      :bbox="box"
      :key="box.id"
      :ref="`box-${box.id}`"
      :selected="isSelected(box.id)"
      :editable="true"
      @selectedBBox="$emit('selectedBBox', $event)"
      @delete="$emit('delete', $event)"
      @edit="$emit('edit', $event)"
      @copy="$emit('copy', $event)"
    />

    <core-BoundingBox
      v-if="currentBBox !== undefined"
      :bbox="currentBBox"
    />

    <core-BoundingBox
      v-if="newBox !== undefined"
      v-model="newBox"
    />

    <v-menu
      v-model="showCtxMenu"
      :position-x="ctxMenuPos.x"
      :position-y="ctxMenuPos.y"
      absolute
      offset-y
    >
      <v-list flat dense subheader>
        <v-subheader>Image actions</v-subheader>

        <v-list-item-group
          color="primary"
        >
        <div v-for="(item, i) in ctxMenuItems" :key="i">
          <v-divider v-if="item.separator"></v-divider>
          <v-list-item v-else
              @click="ctxMenuClicked(item.action)"
              :disabled="item.disabled"
            >
              <v-list-item-icon>
                <v-icon v-text="item.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.text"></v-list-item-title>
              </v-list-item-content>

          </v-list-item>

        </div>
        </v-list-item-group>
      </v-list>
    </v-menu>
  </div>
</template>


<script>
import { mapGetters } from 'vuex'
class Coords{
  constructor(x, y){
    this.x = x;
    this.y = y;
  }

  reset() {
    this.x = undefined;
    this.y = undefined;
  }

  isSet(){
    return this.x !== undefined && this.y !== undefined;
  }
}

export default {
  name: "ImageAnnotations",

  props: {
    fileLabel: undefined,
    bboxes: undefined,
    interaction: undefined,
    selectedBBox: undefined,
  },

  watch: {
    interaction: function(oldInteraction, newInteraction) {
      if (oldInteraction === "add" && newInteraction !== "add") {
        this.x = null;
        this.y = null;
        this.currentBBox = undefined;
      }
    },
  },

  data: () => ({
    minSize: 0,
    initPos: new Coords(),
    currentBBox: undefined,
    toggleBBoxUpdate: false,
    newBox: undefined,
    action: undefined,

    ctxMenuPos: new Coords(0, 0),
    ctxMenuRelPos: new Coords(0, 0),
    showCtxMenu: false,
  }),


  computed: {
    ctxMenuItems() {
      return [
        { text: 'Paste box', icon: 'mdi-content-paste', action: 'paste', disabled: !this.hasBboxStored},
        { text: 'Add box', icon: 'mdi-plus', action: 'add_box' },
        { text: 'Estimate box', icon: 'mdi-circle-box-outline', action: "estimate_bbox"},
        { separator: true },
        { text: 'Classify image', icon: 'mdi-label-multiple-outline', action: "predict"},
        { text: 'Detect boxes', icon: 'mdi-view-grid-plus-outline', action: "detect"},
        { text: 'Annotate', icon: 'mdi-tag', action: "annotate"},
      ]
    },

    ...mapGetters('pastebin', {
      hasBboxStored: 'isSet'
    }),
  },

  methods: {
    ctxMenuClicked(action){
      if (action === "add_box")
        this.initPos = this.ctxMenuRelPos;
      else
        this.$emit(action)
    },

    isSelected(boxId){
      return this.selectedBBox !== undefined && this.selectedBBox.id === boxId;
    },

    getCoordinates(event) {
      var bounds = event.currentTarget.getBoundingClientRect();
      return new Coords(Math.max(event.clientX - bounds.left, 0), Math.max(event.clientY - bounds.top, 0))
    },

    toggleVisibility(boxId){
      if (boxId === undefined)
        return false;

      let comp = this.$refs[`box-${boxId}`][0];
      if (comp === undefined)
        return false;

      comp.hidden = !comp.hidden;
      return comp.hidden;
    },

    highlight(boxId) {
      if (boxId !== undefined)
        this.$refs[`box-${boxId}`][0].highlight = true;
      else
        for (let _box of this.bboxes)
          this.$refs[`box-${_box.id}`][0].highlight = false;
    },


    mouseEnter(e) {
      console.debug('mouseenter');
      this.mouseMove(e)
    },
    mouseLeave(e) {
      console.debug('mouseleave');
      this.mouseMove(e)
    },
    mouseMove(event) {
      if (this.initPos.isSet()) // && this.interaction === "add") {
          this.currentBBox = this.calculateBBox(event);
    },
    mouseClicked() {
      if (this.initPos.isSet()){
        // second click
        this.$emit("addBBox", this.currentBBox)
        this.resetDrawBBox();
      }
        // this.drawBBox(event);
    },

    rightClick(e) {
      this.resetDrawBBox()
      e.preventDefault()
      this.showCtxMenu = false
      this.ctxMenuPos = new Coords(e.clientX, e.clientY)
      this.ctxMenuRelPos = this.getCoordinates(e)
      this.$nextTick(() => {
        this.showCtxMenu = true
      })
    },

    getDisplayLabel(label) {
      if (label !== null) {
        return label;
      } else {
        return "Unknown";
      }
    },

    resetDrawBBox() {
      this.initPos.reset();
      this.currentBBox = undefined;
      console.debug("Reset draw_box")
    },

    calculateBBox(event) {
      let p1 = this.initPos, p2 = this.getCoordinates(event);
      if (!p1.isSet() || !p2.isSet()) {
        return undefined;
      }
      let x1 = p1.x, y1 = p1.y, x2 = p2.x, y2 = p2.y;
      // Scale bounding box coordinates to [0,1].
      var W = this.$refs.overlay.clientWidth
      var H = this.$refs.overlay.clientHeight
      x1 = (x1 + 1) / W;
      x2 = (x2 + 1) / W;
      y1 = (y1 + 1) / H;
      y2 = (y2 + 1) / H;

      // Switch x1 / x2 and y1 / y2 if necessary.
      let x = Math.min(x1, x2), y = Math.min(y1, y2);
      let dx = 1/W, dy = 1/H;
      x += x==x1 ? -dx : dx;
      y += y==y1 ? -dy : dy;
      return {
        width: Math.max(Math.abs(x2 - x1), this.minSize / W),
        height: Math.max(Math.abs(y2 - y1), this.minSize / H),
        x: x,
        y: y,
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
