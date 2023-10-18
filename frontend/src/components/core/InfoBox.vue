<template>
  <div id="info-box">
    <h4>Info</h4>
    {{this.bboxes.length}} Bounding boxes

    <v-virtual-scroll
      class="box-list"
      height="500"
      item-height="75"
      bench="100"
      :items="bboxes"
      >

      <template v-slot:default="{ item }">
        <core-BoundingBoxInfo
          :bbox="item"
          :ref="`box-info-${item.id}`"
          @mouseenter.native="$emit('highlight', item.id)"
          @mouseleave.native="$emit('highlight', undefined)"
          @toggle="$emit('toggle', item)"
          @select="$emit('select', item)"
          @remove="$emit('remove', item)"
        />
      </template>
    </v-virtual-scroll>
    <div v-if="this.selectedBBox === 'asdasd'">
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

  watch: {
    selectedBBox: function(){
      this.updateSelected()
    },

    bboxes: function() {
      this.updateSelected()
    }
  },

  mounted: function() {
    if (this.selectedBBox !== undefined)
      this.markSelected(this.selectedBBox?.id, true)
  },

  methods: {
    updateSelected(){
      for (let box of this.bboxes){
        this.markSelected(box.id, box.id == this.selectedBBox?.id)
      }
    },

    markSelected(boxId, selected){
      let box_info = this.$refs[`box-info-${boxId}`]
      if (box_info !== undefined){
        box_info.selected = selected
        if (selected)
          box_info.$el.scrollIntoView({behavior: "smooth"})
      }
    }
  },
}
</script>

<style scoped>
#info-box {
  background-color: whitesmoke;
}

</style>
