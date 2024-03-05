<template>
  <div align="center">
    <utils-KeypressHandler @pressed="handleKeyPress($event)"/>

    <dialogs-BoundingBoxDelete
      :box="boxSelection.toDelete"
      :file="file"
      @close="boxSelection.toDelete = undefined"
      @confirm="removeBBox($event)"
    />

    <dialogs-BoundingBoxEdit
      :box="boxSelection.toEdit"
      :file="file"
      @close="boxSelection.toEdit = undefined"
      @confirm="updateBBox($event)"
    />

    <dialogs-AnnotationDialog
      v-model="showAnnotationDialog"
      @selected="annotate($event)"
    />

    <v-row>
      <v-col>

        <core-LazyImage
          :file="file"
          thumbSize="large"
          :maxHeight="maxHeight"
        >

          <core-ImageAnnotations
            ref="imageAnnotations"
            :fileLabel="file.label"
            :bboxes="bboxes"
            @addBBox="addBBox($event)"
            :selectedBBox="boxSelection.selected"
            @selectedBBox="bboxClicked($event)"
            @delete="boxSelection.toDelete = $event"
            @edit="boxSelection.toEdit = $event"
          />
        </core-LazyImage>
      </v-col>

      <v-col cols="3">
        <core-InfoBox
          ref="infoBox"
          :selectedBBox="boxSelection.selected"
          :bboxes="bboxes"
          :file="file"
          :maxHeight="maxHeight / 2"
          @highlight="$refs.imageAnnotations.highlight($event)"
          @toggle="toggle($event)"
          @select="select($event)"
          @remove="boxSelection.toDelete = $event"

          @annotate="showAnnotationDialog = true"
          @predict="classify($event)"
          @detect="detect($event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>

import DataService from '@/services/data.service';
import { mapGetters } from 'vuex'

class BoxSelection{
  selected = undefined;
  toDelete = undefined;
  toEdit = undefined;

  reset(){
    this.selected = undefined;
    this.toDelete = undefined;
    this.toEdit = undefined;
  }

  delete(){
    this.toDelete = this.selected;
  }

  edit(){
    this.toEdit = this.selected;
  }

  select(box){
    this.selected = box;
  }
}

export default {
  name: "ImageAnnotator",

  props: {
    file: undefined,
    maxHeight: {
      type: Number,
      default: () => 600
    },
  },

  data: () => ({
    // interaction: undefined, // default interaction
    boxSelection: new BoxSelection(),

    showAnnotationDialog: false,

    bboxes: [],

    keyActions: {

      ArrowRight(that){
        that.$emit("next")
      },

      ArrowLeft(that){
        that.$emit("previous")
      },

      Delete(that){
        that.closeDialog()
        that.boxSelection.delete();
      },

      Escape(that){
        if (that.isDialogOpen)
          that.closeDialog()
        that.$refs.imageAnnotations.resetDrawBBox()
      },

      Enter(that) {
        if (that.isDialogOpen)
          that.confirmDialog()
      },

      c(that, event){
        if(!event.ctrlKey)
          return
        if(that.boxSelection.selected === undefined)
          return
        that.sendToPastebin(that.boxSelection.selected);
      },

      v(that, event){
        if(!event.ctrlKey)
          return
        that.getFromPastebin();
      },

    },
  }),

  created: function () {
    this.getBBoxes();
  },

  watch: {
    file: function(){
      this.getBBoxes();
      this.boxSelection.reset();
    }
  },

  computed: {
    fileId: function() {
      return this.file.id;
    },

    isDialogOpen: function () {
      return this.boxSelection.toDelete !== undefined || this.boxSelection.toEdit !== undefined;
    },

    ...mapGetters('pastebin', {
      storedBbox: 'get',
      hasBboxStored: 'isSet'
    }),
  },


  methods: {
    getFromPastebin() {
      if(!this.hasBboxStored){
        this.$store.dispatch("messages/alert", {msg: "No box stored in pastebin.", timeout: 1500})
        return
      }
      let bbox = this.storedBbox;
      console.log("Got box from pastebin: ", bbox)
      this.pasteBox(bbox)
    },

    pasteBox(bbox) {
      if(this.hasOverlap(bbox, 0.5))
        return this.$store.dispatch("messages/alert", {msg: "Pasted box has to much overlap with another box!", timeout: 1500})

      this.addBBox(bbox, bbox.label)
      this.$store.dispatch("messages/info", {msg: "Pasted box from pastebin.", timeout: 1500})
    },

    hasOverlap(bbox, thresh){
      return this.bboxes.some( box => box.iou(bbox) > thresh);
    },

    sendToPastebin(bbox){
      if (bbox === undefined){
        console.error("[ImageAnnotator] No box selected for pastebin.")
        return
      }
      this.$store.dispatch("messages/info", {msg: "Copied selected box", timeout: 1500})
      this.$store.dispatch("pastebin/store", bbox)
      console.log("Copied selected bbox!", bbox)
    },

    closeDialog(){
      this.boxSelection.toDelete = undefined;
      this.boxSelection.toEdit = undefined;
    },

    confirmDialog(){
      if (this.boxSelection.toDelete !== undefined)
        return this.removeBBox(this.boxSelection.toDelete)
      if (this.boxSelection.toEdit !== undefined)
        return this.updateBBox(this.boxSelection.toEdit)
    },

    handleKeyPress(event){
      // ignore key presses if the annotationed dialog is open
      if (this.showAnnotationDialog)
        return

      for (let key in this.keyActions)
        if (event.key == key)
          this.keyActions[key](this, event)
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

    classifyAll(){
      DataService.files.predict_bboxes(this.fileId)
        .then((task) => {
          if (task === undefined){
            console.error("[Image Annotator] Failed to predict bounding boxes.");
            return
          }
          this.$store.commit("addTask", task);
          this.$emit('updateBboxes');
          this.getBBoxes();
      });

      this.$store.dispatch("messages/info", {msg: "Classifier started"})
    },

    classifyBbox(bboxId){
      DataService.bboxes.predict(bboxId)
        .then((task) => {
          if (task === undefined){
            console.error("[Image Annotator] Failed to predict bounding box.");
            return;
          }
          this.$store.commit("addTask", task);
          this.$emit('updateBboxes');
          this.getBBoxes();
      });
      this.$store.dispatch("messages/info", {msg: "Classifier started"})
    },

    classify(bbox){
      if (bbox === undefined)
        return this.classifyAll()
      else
        return this.classifyBbox(bbox?.id)
    },

    detect() {
      DataService.files.generate_bboxes(this.fileId)
        .then((ok) => {
          if (!ok){
            console.error("[Image Annotator] Failed to add generate bounding boxes.");
          }
          this.getBBoxes();
        });
    },

    annotate(label){
      let bbox = this.boxSelection.selected;
      if (bbox === undefined){
        console.warn("[Image Annotator] no bbox was selected for annotation!", label)
        return

      }

      console.log("[Image Annotator] bbox labeling triggered", bbox, label)
      DataService.bboxes.setLabel(bbox.id, label)
        .then((ok) => {
          if (!ok){
            console.error("[Image Annotator] Failed to label bounding box.");
          }
          this.$emit('updateBboxes');
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
          this.boxSelection.toDelete = undefined;
        });
    },

    updateBBox(bbox){
      DataService.bboxes.update(bbox)
        .then((ok) => {
          if (!ok){
            console.log("Failed to update bounding box.");
          }
          this.getBBoxes();
          this.boxSelection.toEdit = undefined;
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
      if(this.$refs.infoBox !== undefined)
        this.$refs.infoBox.markHidden(bbox?.id, hidden)
    },

    select(bbox){
      if(this.boxSelection.selected?.id == bbox.id)
        this.boxSelection.reset()
      else
        this.boxSelection.select(bbox)
    },

    getBBoxes() {
      DataService.bboxes.get(this.fileId)
        .then((bboxes) => {
          this.bboxes = bboxes;

          let showInfo = this.$route.query?.showInfo;
          if (showInfo !== undefined){
            let box = this.bboxes.find((box) => box.id == showInfo);

            this.boxSelection.select(box);
          }
        });
      // this.toggleBBoxUpdate=!this.toggleBBoxUpdates; // toggle to change key and trigger update
    },

    bboxClicked(bbox) {
      console.log("Clicked on", bbox?.id)

      // // Manage corresponding interactions.
      if (bbox === undefined)
        return;
      this.select(bbox);

    }
  }
}
</script>
