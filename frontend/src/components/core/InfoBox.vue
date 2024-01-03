<template>
  <v-card
    dense
    elevation="2"
    id="info-box"
    :max-height="maxHeight">
    <v-card-title>File info</v-card-title>
    <v-card-text>
      <v-simple-table class="info-table">
        <template v-slot:default>
          <thead>
          </thead>
          <tbody>
            <tr>
              <th width="50%" class="text-left">File name</th>
              <td class="text-right">{{file.name}}</td>
            </tr>
            <tr>
              <th class="text-left">Bounding boxes</th>
              <td class="text-right">{{bboxes.length}}</td>
            </tr>
            <tr v-if="file.label">
              <th class="text-left">File label</th>
              <td class="text-right">{{file.label || "Not annotated"}}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card-text>

    <v-card-title>Annotations</v-card-title>

    <v-card-text>
      <v-virtual-scroll
        class="box-list"
        height="350"
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
    </v-card-text>
  </v-card>
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
