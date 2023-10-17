<template>
  <div id="info-box">
    <h4>Info</h4>

    <div id="box-list">
      {{this.bboxes.length}} Bounding boxes
      <v-virtual-scroll
        :items="bboxes"
        height="500"
        item-height="35"
        >

        <template v-slot:default="{ item }">
          <core-BoundingBoxInfo
            :bbox="item"
            @mouseenter.native="$emit('highlight', item.id)"
            @mouseleave.native="$emit('highlight', undefined)"
            @toggle="$emit('toggle', item)"
            @select="$emit('select', item)"
            @remove="$emit('remove', item)"
          />
        </template>
      </v-virtual-scroll>
      </div>

    <div v-if="this.selectedBBox !== undefined">
      Bounding box: #{{ this.selectedBBox.id }} <br>
      Label: {{ this.selectedBBox.label }} <br>
      Predicted Label: {{ this.selectedBBox.predicted_label }} (by: {{ this.selectedBBox.prediction_model }}) <br>
      Confirmators: {{ this.selectedBBox.confirmators }}
    </div>
  </div>
</template>

<script>

export default {
  name: "InfoBox",
  props: {
    bboxes: undefined,
    selectedBBox: undefined,
    maxHeight: undefined,
  },
  data: () => ({
  }),

  methods: {

  }
}
</script>

<style scoped>
#info-box {
  background-color: whitesmoke;
}
</style>
