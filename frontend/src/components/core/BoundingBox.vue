<template>
  <div
    class="bounding-box"
    :style="style"
    :class="{highlighted: highlightId === localValue.id, pipeline: localValue.pipelineGenerated}"
    @click="$emit('selectedBBox', localValue)"
  >
    <v-chip
      label x-small
      :class="{highlighted: highlightId === localValue.id}"
    >
      {{getLabel}}
    </v-chip>
  </div>
</template>

<script>

export default {
  name: "BoundingBox",
  model: {prop: "value", event: "input"},

  props: {
    value: undefined,
    highlightId: undefined,
  },

  computed: {
    localValue: {
      get: function(){ return this.value },
      set: function(value){ this.$emit('input', value) },
    },

    style: function() {
      return {
        top: `${this.value.y * 100}%`,
        left: `${this.value.x * 100}%`,
        width: `${this.value.width * 100}%`,
        height: `${this.value.height * 100}%`,
        // Label: localValue.label
      }
    },

    getLabel: function() {
      if ((typeof this.value.label !== 'undefined' && this.value.label !== null) || (typeof this.value.predicted_label !== 'undefined' && this.value.predicted_label !== null)) {
        if (this.value.label !== null) {
          return this.value.label;
        } else {
          return this.value.predicted_label;
        }
      } else {
        return "Unknown";
      }
    }
  },

}

</script>


<style scoped>
  .bounding-box{
    position: absolute;

    background-color: rgba(0, 0, 255.0, 0.3);
    color: whitesmoke;
  }

  .bounding-box:hover{
    background-color: rgba(0, 0, 255.0, 0.4);
  }

  .bounding-box.pipeline{
    background-color: rgba(0.0, 126.0, 0.0, 0.4);
  }

  .bounding-box.highlighted{
    background-color: rgba(148.0, 0, 211.0, 0.4);
  }
</style>
