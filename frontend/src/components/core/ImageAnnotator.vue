<template>
    <div align="center">
      <v-row>
        <v-col cols="auto">
          <core-ImageAnnotatorOptionBar
            :interaction="interaction"
            @interaction="setInteraction($event)"
            @reset="resetInteraction()"
          />
        </v-col>

        <v-col>
          <div v-if="(interaction === 'info-box' || interaction == 'confirm-box' || interaction === 'label-box' || interaction === 'predict-box') && typeof selectedBBox !== 'undefined'">
            <h4>Selected Bounding Box:</h4>
            Label: {{ this.selectedBBox.label }} <br>
            Predicted Label: {{ this.selectedBBox.predicted_label }} (by: {{ this.selectedBBox.prediction_model }}) <br>
            Confirmators: {{ this.selectedBBox.confirmators }}
          </div>

          <core-LazyImage
            :file="file"
            thumbSize="large"
            maxHeight="675"
          >

            <core-ImageAnnotations
              ref="imageAnnotations"
              :interaction="interaction"
              :fileLabel="file.label"
              :fileId="file.id"
              :selectedBBox="selectedBBox"
              @selectedBBox="selectBBox($event)"
            />
          </core-LazyImage>
        </v-col>
      </v-row>
    </div>
</template>

<script>
export default {
  name: "ImageAnnotator",

  props: {
    file: undefined
  },

  data: () => ({
    interaction: 'draw-box',
    selectedBBox: undefined,
  }),

  methods: {
    setInteraction(interaction) {
      this.interaction = interaction;

      if (!(interaction === "info-box" || interaction === "label-box" || interaction === "confirm-box") && typeof this.selectedBBox !== 'undefined') {
        this.selectedBBox = undefined;
      }
      if (interaction === "generate-box") {
        this.$refs.imageAnnotations.generateBBoxes();
      }
    },
    resetInteraction() {
      if (this.interaction === "draw-box") {
        this.$refs.imageAnnotations.resetDrawBBox();
      }
    },
    selectBBox(event) {
      // Set selected BBox.
      this.selectedBBox = event;

      // Manage corresponding interactions.
      if (typeof this.selectedBBox === 'undefined') {
        return;
      } else if (this.interaction === "remove-box") {
        this.$refs.imageAnnotations.removeBBox(this.selectedBBox);
      } else if (this.interaction === "label-box") {
        this.$refs.imageAnnotations.labelBBox(this.selectedBBox, "Dummy label 2");
      } else if (this.interaction === "predict-box") {
        this.$refs.imageAnnotations.predictBBox(this.selectedBBox);
      } else if (this.interaction === "confirm-box") {
        this.$refs.imageAnnotations.confirmBBox(this.selectedBBox);
      }
    }
  }
}
</script>
