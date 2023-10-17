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
  model: {prop: "bbox", event: "input"},

  props: {
    bbox: undefined,
  },

  data: () => ({
    selected: false,
    highlight: false,
    hidden: false,
  }),

  computed: {
    localValue: {
      get: function(){ return this.bbox },
      set: function(bbox){ this.$emit('input', bbox) },
    },

    style: function() {
      // let alpha = this.hovered ? 0.4 : 0.3;
      // let color = this.hovered ? 0.4 : 0.3;

      return {
        top: `${this.bbox.y * 100}%`,
        left: `${this.bbox.x * 100}%`,
        width: `${this.bbox.width * 100}%`,
        height: `${this.bbox.height * 100}%`,
        // Label: localValue.label
      }
    },

    getLabel: function() {
      if (this.hasLabel) {
        if (this.bbox.label !== null) {
          return this.bbox.label;
        } else {
          return this.bbox.predicted_label;
        }
      } else {
        return "Unknown";
      }
    },

    hasLabel: function(){
      return (typeof this.bbox.label !== 'undefined' && this.bbox.label !== null) || (typeof this.bbox.predicted_label !== 'undefined' && this.bbox.predicted_label !== null);
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
    display: initial;
  }

  .bounding-box.highlight.hidden{
    border-style: dotted;
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
