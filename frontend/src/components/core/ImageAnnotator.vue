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
      <v-col cols="auto">
        <core-ImageAnnotatorOptionBar
          ref="optionBar"
          :interaction="interaction"
          @action="setInteraction($event)"
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
            :selectedBBox="boxSelection.selected"
            @selectedBBox="bboxClicked($event)"
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
    interaction: 'select',
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
        if (that.state === "dialog")
          that.closeDialog()
        else
          that.interaction = "select"
      },

      Enter(that) {
        if (that.state === "dialog")
          that.confirmDialog()
      },

      v(that){
        that.toggle(that.boxSelection.selected);
      },

      e(that){
        that.closeDialog()
        that.boxSelection.edit();
        that.interaction = "edit"
      },
      a(that){
        that.interaction = "add"
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

    state: function() {
      if (this.isDialogOpen)
        return "dialog";
      else
        return this.interaction;
    },

    isDialogOpen: function () {
      return this.boxSelection.toDelete !== undefined || this.boxSelection.toEdit !== undefined;
    }
  },


  methods: {

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
          this.keyActions[key](this)
    },

    setInteraction(interaction) {

      if (interaction === "add"){
        // unselect the bbox if it is set
        this.select(this.selectedBBox);
      }

      else if (interaction === "delete"){
        this.boxSelection.delete()
        // because we do not want to change the interaction mode
        interaction = this.interaction;
      }

      else if (interaction === "detect") {
        this.detect();
      }

      else if (interaction === "classify") {
        interaction = "pipeline";
        this.classify(this.boxSelection.selected)
      }

      else if (interaction === "classify-all") {
        interaction = "pipeline";
        this.classify()
      }

      if (interaction === this.interaction)
        return

      console.log("[Image Annotator] setting new interaction:", this.interaction)
      this.interaction = interaction;
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
      DataService.bboxes.set_label(bbox.id, label)
        .then((ok) => {
          if (!ok){
            console.error("[Image Annotator] Failed to label bounding box.");
          }
          this.$emit('updateBboxes');
          this.getBBoxes();
        });
    },

    // labelBBox(bbox, label) {
    //   DataService.bboxes.set_label(bbox.id, label)
    //     .then((ok) => {
    //       if (!ok){
    //         console.error("[Image Annotator] Failed to label bounding box.");
    //       }
    //       this.$emit('updateBboxes');
    //       this.getBBoxes();
    //     });
    // },

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
      console.log("Clicked on", bbox?.id, "current mode:", this.interaction)

      // // Manage corresponding interactions.
      if (bbox === undefined || this.interaction === "add")
        return;
      this.select(bbox);

      if (this.interaction === "edit")
        return this.boxSelection.edit()

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
