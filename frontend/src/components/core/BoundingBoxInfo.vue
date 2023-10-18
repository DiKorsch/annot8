<template>
  <v-list-item
    dense class="bbox-info" :class="{selected}"
    @click="$emit('select', bbox.id)"
  >
    <v-list-item-content class="label" >
      <v-list-item-title>#{{this.bbox.id}}</v-list-item-title>
      <div v-if="this.has_label">Label: {{this.label}}</div>
      <div v-if="selected">MORE INFO</div>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn-toggle dense borderless>
      <v-icon
        small
        class="info-button"
        @click.stop="$emit('toggle', bbox.id)">mdi-eye-outline
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
export default {
  name: "BoundingBoxInfo",
  model: {prop: "bbox", event: "input"},

  props: {
    bbox: undefined,
  },

  data: () => ({
    selected: false,
  }),

  computed: {
    localValue: {
      get: function(){ return this.bbox },
      set: function(bbox){ this.$emit('input', bbox) },
    },

    label: function() {
      return this.bbox.label || this.bbox.predicted_label;
      // if (label === null || label === undefined)
      //   return `#${this.bbox.id}`
      // else
      //   return `#${this.bbox.id}: ${label}`
    },
    has_label: function(){
      let lab = this.label;
      return lab !== undefined && lab !== null ;
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
}
</style>
