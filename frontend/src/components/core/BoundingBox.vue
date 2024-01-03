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
    <v-tooltip top>

      <template v-slot:activator="{ on, attrs }">
        <div v-if="hasLabel"
          v-bind="attrs"
          v-on="on"
          class="label lighten-1"
          :class="{
            blue: localValue.label !== null,
            green: localValue.label === null,
          }"
          >
          <v-icon small v-if="localValue.label !== null">mdi-tag</v-icon>
          <v-icon small v-else>mdi-brain</v-icon>
        </div>
      </template>
      <span>{{labelName}}</span>
    </v-tooltip>
  </div>
</template>

<script>

export default {
  name: "BoundingBox",
  model: {prop: "bbox", event: "input"},

  props: {
    bbox: undefined,
    selected: {
      type: Boolean,
      default: false
    },
  },

  data: () => ({
    highlight: false,
    hidden: false,
  }),

  computed: {
    localValue: {
      get: function(){ return this.bbox },
      set: function(bbox){ this.$emit('input', bbox) },
    },

    style: function() {

      return {
        top: `${this.bbox.y * 100}%`,
        left: `${this.bbox.x * 100}%`,
        width: `${this.bbox.width * 100}%`,
        height: `${this.bbox.height * 100}%`,
        // Label: localValue.label
      }
    },

    labelName: function() {
      if (this.hasLabel) {
        if (this.bbox.label !== null) {
          return this.bbox.label.name;
        } else {
          return this.bbox.predicted_label.name;
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
  .bounding-box .label {
    opacity: 80%;
    position: absolute;
    inset: -12px -12px auto auto ;
    height: 24px;
    width: 24px;
    border-radius: 24px;
    border-width: 1px;
    border-style: solid;
    border-color: black !important;
    display: flex;
    justify-content: center;
    text-align: center;
  }

  .bounding-box.selected .label, .bounding-box.highlight .label{
    inset: -13px -13px auto auto ;
  }

  .bounding-box.hidden{
    display: none;
  }

  .bounding-box {
    position: absolute;

    background-color: rgba(0, 0, 255.0, 0.3);
    color: whitesmoke;
    border-width: 1px;
    border-style: solid;
    border-color: rgba(0, 0, 0, 0.6);;
    padding: 2px;
  }


  .bounding-box.selected, .bounding-box.highlight{
    border-width: 2px;
    padding: 1px;
    display: initial;
  }

  .bounding-box.highlight{
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  }

  .bounding-box.selected.hidden, .bounding-box.highlight.hidden{
    border-style: dotted;
  }

  .bounding-box.selected.hidden .label, .bounding-box.highlight.hidden .label{
    border-style: dotted;
  }

  .bounding-box:hover{
    background-color: rgba(0, 0, 255.0, 0.4);
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
  }

  .bounding-box.pipeline{
    background-color: rgba(0.0, 126.0, 0.0, 0.3);
  }

  .bounding-box.pipeline:hover{
    background-color: rgba(0.0, 126.0, 0.0, 0.4);
  }

</style>
