<template>
  <v-expansion-panels accordion hover v-model="panel">
    <v-expansion-panel>
      <v-expansion-panel-header>File</v-expansion-panel-header>
      <v-expansion-panel-content>
        <core-FileInfo
          :file="file"
          :bboxes="bboxes"
          :annotateButton="false"
          :deleteButton="false"
        />
      </v-expansion-panel-content>
    </v-expansion-panel>


    <v-expansion-panel>
      <v-expansion-panel-header>Boxes</v-expansion-panel-header>
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
      <v-expansion-panel-header>Selected Box</v-expansion-panel-header>
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
    }
  },
}
</script>

<style scoped>
  .clickable {
    cursor: pointer;
  }

</style>
