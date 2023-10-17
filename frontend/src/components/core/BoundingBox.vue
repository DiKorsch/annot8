<template>
  <div
    class="bounding-box"
    :style="style"
    :class="{
        pipeline: localValue.pipelineGenerated,
        selected: selected,
        highlight: highlight,
        hidden: hidden}"
    @click="$emit('selectedBBox', localValue)"
  >
    <v-chip v-if="hasLabel"
      label x-small
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
  },

  data: () => ({
    selected: false,
    highlight: false,
    hidden: false,
  }),

  computed: {
    localValue: {
      get: function(){ return this.value },
      set: function(value){ this.$emit('input', value) },
    },

    style: function() {
      // let alpha = this.hovered ? 0.4 : 0.3;
      // let color = this.hovered ? 0.4 : 0.3;

      return {
        top: `${this.value.y * 100}%`,
        left: `${this.value.x * 100}%`,
        width: `${this.value.width * 100}%`,
        height: `${this.value.height * 100}%`,
        // Label: localValue.label
      }
    },

    getLabel: function() {
      if (this.hasLabel) {
        if (this.value.label !== null) {
          return this.value.label;
        } else {
          return this.value.predicted_label;
        }
      } else {
        return "Unknown";
      }
    },

    hasLabel: function(){
      return (typeof this.value.label !== 'undefined' && this.value.label !== null) || (typeof this.value.predicted_label !== 'undefined' && this.value.predicted_label !== null);
    }
  },

  methods: {
    handleLeftClick: function(e) {
      console.log("left click box:", e)
    },
    handleRightClick: function(e) {
      console.log("right click box:", e)
    },

  },

}

</script>


<style scoped>
  .bounding-box.hidden{
    display: none;
  }

  .bounding-box{
    position: absolute;

    background-color: rgba(0, 0, 255.0, 0.3);
    color: whitesmoke;
    border-width: 1px;
    border-style: solid;
    border-color: rgba(0, 0, 0, 0.6);;
  }


  .bounding-box.selected, .bounding-box.highlight{
    border-width: 2px;
  }

  .bounding-box:hover{
    background-color: rgba(0, 0, 255.0, 0.4);
  }

  .bounding-box.pipeline{
    background-color: rgba(0.0, 126.0, 0.0, 0.3);
  }

  .bounding-box.pipeline:hover{
    background-color: rgba(0.0, 126.0, 0.0, 0.4);
  }

  .bounding-box.highlighted{
/*    background-color: rgba(148.0, 0, 211.0, 0.4);*/
  }

  .bounding-box.hovered{
/*    background-color: rgba(148.0, 120, 211.0, 0.4);*/
  }

  .box-label {
    /*position: absolute;
    left: 2px;
    top: 2px;*/
  }
</style>
