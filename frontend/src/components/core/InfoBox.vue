<template>
  <div>
    <h2>Operations on ...</h2>
    <v-expansion-panels accordion hover v-model="panel">
      <v-expansion-panel>
        <v-expansion-panel-header><h3>Image</h3></v-expansion-panel-header>
        <v-expansion-panel-content>
          <core-FileInfo
            :file="file"
            :bboxes="bboxes"
            :annotateButton="false"
            :deleteButton="false"
          />
          <v-divider></v-divider>
          <v-btn @click="$emit('detect')" small title="Run detector on this file">
            <v-icon left>mdi-view-grid-plus-outline</v-icon> Detect
          </v-btn>
          <v-menu offset-y>

            <template v-slot:activator="{ on, attrs }">
              <v-btn
                small
                v-bind="attrs"
                v-on="on"
                title="Run classifier on the image or detected boxes"
              >
                <v-icon left>mdi-label-multiple-outline</v-icon> Classify
              </v-btn>
            </template>

            <v-list>
              <v-list-item link @click="$emit('predictImage')">
                <v-icon left>mdi-label-outline</v-icon> Image
              </v-list-item>
              <v-list-item link @click="$emit('predict')" :disabled="!hasBboxes" >
                <v-icon left>mdi-label-multiple-outline</v-icon> All boxes
              </v-list-item>
            </v-list>
          </v-menu>

          <v-btn @click="$emit('annotateImage')" small title="Give this image a label">
            <v-icon left>mdi-tag</v-icon> Annotate
          </v-btn>
        </v-expansion-panel-content>
      </v-expansion-panel>


      <v-expansion-panel v-if="hasBboxes">
        <v-expansion-panel-header><h3>Bounding boxes</h3></v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-virtual-scroll
            class="box-list"
            :max-height="maxHeight"
            item-height="75"
            bench="100"
            :items="bboxes"
            >

            <template v-slot:default="{ item }">
              <core-BoundingBoxListItem
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
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel v-if="selectedBBox !== undefined">
        <v-expansion-panel-header><h3>Selected box</h3></v-expansion-panel-header>
        <v-expansion-panel-content>
          <core-BoundingBoxInfo
            :bbox="selectedBBox"
            :maxHeight="maxHeight"
            @annotate="$emit('annotate', $event)"
            @predict="$emit('predict', $event)"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
export default {
  name: "InfoBox",
  props: {
    bboxes: undefined,
    file: undefined,
    selectedBBox: undefined,
    maxHeight: undefined,
  },
  data: () => ({
    panel: undefined
  }),

  watch: {
    selectedBBox: function(){
      this.updateSelected()
      this.panel = 2;
    },

    bboxes: function() {
      this.updateSelected()
    }
  },

  mounted: function() {
    if (this.selectedBBox !== undefined){
      this.markSelected(this.selectedBBox?.id, true)
    }
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
    },
    markHidden(boxId, hidden){
      let box_info = this.$refs[`box-info-${boxId}`]
      if (box_info !== undefined)
        box_info.hidden = hidden
    }
  },

  computed: {
    file_name() {
      return this.file?.name;
    },

    hasBboxes() {
      return this.bboxes !== undefined && this.bboxes.length !== 0
    }
  },
}
</script>

<style scoped>
  .clickable {
    cursor: pointer;
  }

</style>
