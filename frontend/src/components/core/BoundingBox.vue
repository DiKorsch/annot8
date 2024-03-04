<template>
  <div>
    
  <div
    class="bounding-box"
    :style="style"
    :class="{
        pipeline: localValue.pipelineGenerated,
        selected: selected,
        highlight: highlight,
        hidden: hidden}"
    @click.stop="$emit('selectedBBox', localValue)"
    @contextmenu.stop="handleRightClick"
  >
    <v-tooltip top v-if="hasLabel">

      <template v-slot:activator="{ on, attrs }">
        <div
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
      <span>{{label}}</span>
    </v-tooltip>
  </div>

  <v-menu
      v-model="showCtxMenu"
      :position-x="ctxMenuX"
      :position-y="ctxMenuY"
      absolute
      offset-y
    >
      <v-list flat dense subheader>
        <v-subheader>Box actions</v-subheader>
        
        <v-list-item-group
          color="primary"
        >
        <div v-for="(item, i) in items" :key="i">
          <v-divider v-if="item.separator"></v-divider>

          <v-list-item v-else
            @click="$emit(item.action, localValue)"
          >
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </div>
        </v-list-item-group>
      </v-list>
    </v-menu>
    
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
    editable: {
      type: Boolean,
      default: false
    },
  },

  data: () => ({
    highlight: false,
    hidden: false,
    ctxMenuX: 0,
    ctxMenuY: 0,
    showCtxMenu: false,
    items: [
      { text: 'Edit', icon: 'mdi-pencil', action: "edit"},
      { text: 'Delete', icon: 'mdi-trash-can', action: "delete"},
      { text: 'Predict', icon: 'mdi-brain', action: "predict"},
      { text: 'Annotate', icon: 'mdi-tag', action: "annotate"},
    ],
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

    label: function() {
      if (this.hasLabel) {
        let label = this.bbox?.label || this.bbox?.predicted_label
        if (label !== null)
          return label.name;
         else
          return "Unknown";
      } else
        return "Unknown";
    },

    hasLabel: function(){
      return (this.bbox.label !== undefined && this.bbox.label !== null) || (this.bbox.predicted_label !== undefined && this.bbox.predicted_label !== null);
    }
  },

  methods: {
    
    handleRightClick: function(e) {
      e.preventDefault()
      if(!this.selected)
        this.$emit('selectedBBox', this.localValue)

      if (!this.editable)
        return
    
      this.showCtxMenu = false
      this.ctxMenuX = e.clientX
      this.ctxMenuY = e.clientY
      this.$nextTick(() => {
        this.showCtxMenu = this.selected
      })
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
