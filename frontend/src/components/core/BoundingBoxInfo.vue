<template>
  <v-list-item
    dense class="bbox-info" :class="{selected}"
    @click="$emit('select', bbox.id)"
  >
    <v-list-item-content class="label" >
      <v-img
        max-height="60"
        contain
        :src="thumb"
        position="center left"
      >#{{this.bbox.id}}</v-img>
      <div v-if="this.has_label">Label: {{this.label}}</div>
      <div v-if="selected">MORE INFO</div>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn-toggle dense borderless>
      <v-icon
        small
        class="info-button"
        @click.stop="$emit('toggle', bbox.id)">
          {{ this.hidden ? 'mdi-eye-off' : 'mdi-eye-outline' }}
      </v-icon>
      <v-icon
        small
        class="info-button"
        @click.stop="$emit('remove', bbox.id)">mdi-trash-can-outline
      </v-icon>
      </v-btn-toggle>
    </v-list-item-action>
  </v-list-item>
</template>


<script>
import { mapGetters } from 'vuex';

export default {
  name: "BoundingBoxInfo",
  model: {prop: "bbox", event: "input"},

  props: {
    bbox: undefined,
  },

  data: () => ({
    selected: false,
    hidden: false,
    thumbSize: "original"
  }),

  computed: {
    ...mapGetters(['getMediaUrl']),
    localValue: {
      get: function(){ return this.bbox },
      set: function(bbox){ this.$emit('input', bbox) },
    },

    label: function() {
      return this.bbox.label || this.bbox.predicted_label;
    },
    has_label: function(){
      let lab = this.label;
      return lab !== undefined && lab !== null ;
    },
    thumb: function() {

      let boxThumbs = this.bbox?.crops;
      let url = ""
      if (boxThumbs !== undefined && boxThumbs[this.thumbSize] !== undefined )
        url = boxThumbs[this.thumbSize]

      return `${this.getMediaUrl}${url}`
    }
  }
}
</script>


<style scoped>
.bbox-info {
  padding: 3px;
}
.bbox-info.selected {
  background-color: rgba(0, 0, 0, 0.1);
  border-style: solid;
  border-width: 1px;
  padding: 2px;
}
.bbox-info .info-button {
  margin: 2px 5px;
}
.bbox-info .label {
  font-size: smaller;
  flex-wrap: nowrap;
  padding: 0px 0px;
}
</style>
