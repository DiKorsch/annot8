<template>
  <div class="action-container">

    <v-btn-toggle dense v-model="action" class="action-buttons">
      <v-btn v-for="button in buttons"
          class="action-btn"
          :key="button.action"
          :ref="`btn-${button.action}`"
          :value="button.action"
          :title="button.title()"
          @click="setAction(button.action)"
      >
        <v-icon :color="action === button.action ? 'accent' : 'primary'">
          mdi-{{button.icon}}
        </v-icon>
      </v-btn>
    </v-btn-toggle>

    <v-btn-toggle dense multiple v-model="active_options" class="action-buttons" >
      <v-btn v-for="button in options"
          class="action-btn"
          :key="button.action"
          :ref="`btn-${button.action}`"
          :value="button.action"
          :title="button.title()"
          @click="$emit(button.action)"
      >
        <v-icon :color="active_options.includes(button.action) ? 'accent' : 'primary'">
          mdi-{{button.icon}}
        </v-icon>
      </v-btn>
    </v-btn-toggle>

    <v-btn-toggle dense class="action-buttons" v-model="modeAction">
      <v-btn v-for="button in current_mode_buttons"
          class="action-btn"
          :key="button.action"
          :ref="`btn-${button.action}`"
          :value="button.action"
          :title="button.title()"
          @click="setModeAction(button.action, button.is_immediate)"
      >
        <v-icon :color="modeAction === button.action ? 'accent' : 'primary'">
          mdi-{{button.icon}}
        </v-icon>
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<script>
// help: https://pictogrammers.github.io/@mdi/font/6.9.96/
// option-bar from pycs

class Button {
  constructor(action, text, icon, key=undefined, is_immediate=false){
    this.action = action
    this.text = text
    this.icon = icon
    this.key = key
    this.is_immediate = is_immediate
  }

  title(){
    if (this.key !== undefined)
      return `${this.text} (${this.key})`
    else
      return this.text
  }
}

export default {
  props: {
    interaction: undefined
  },

  data: () => ({

    buttons: [
      new Button("select", "Select bounding box", "button-pointer", "Escape"),
      new Button("add", "Add bounding box", "shape-square-plus", "a"),
      new Button("edit", "Edit", "lead-pencil", "e"),
      new Button("pipeline", "Open Pipeline", "brain", "p"),
    ],

    mode_buttons: {
      add: [
        new Button("draw-box", "Draw bounding box", "vector-rectangle", "d"),
        new Button("extreme-clicking", "Extreme Clicking", "cursor-default-click-outline", "e"),
        new Button("estimate", "Estimate bounding box", "auto-fix", "a"),
        new Button("copy", "Copy from previous image", "content-copy", "c"),
      ],
      edit: [
        new Button("confirm-all", "Cofirm all bounding boxes", "check-all", "a"),
        new Button("label", "Label image", "label-outline", "l"),
      ],
      pipeline: [
        new Button("detect", "Detect insects", "view-grid-plus-outline", "d", true),
        new Button("classify", "Classify bounding box", "label-outline", "c"),
        new Button("classify-all", "Classify all boxes", "label-multiple-outline", "p"),
        new Button("detect-classify", "Detect and classify everything", "plus-box-multiple-outline", "a"),
      ],
    },
    options: [
      new Button("toggleInfoBox", "Show info box", "information-outline", "i"),
    ],
    modeAction: undefined,
    active_options: [],
  }),

  methods: {

    setAction: function(action){
      this.action = action
    },

    setModeAction: function(action, is_immediate = false){
      if (is_immediate)
        this.modeAction = undefined
      else
        this.modeAction = action
      this.$emit("action", action)
    },

    toggleOption: function(value, add){
      if (add)
        this.active_options.push(value)
      else
        this.active_options.pop(value)
    }

  },

  computed: {
    current_mode_buttons(){
      return this.mode_buttons[this.action] || []
    },

    action: {
      get() {
        return this.interaction;
      },
      set(value) {
        this.$emit("action", value)
      }
    }
  },

  watch: {
    // action: function(newaction){
    //   if (newaction === undefined)
    //     this.action = "select"
    //   this.modeAction = undefined
    // }
  }
}
</script>

<style scoped>
.action-container {
  display: flex;
  flex-direction: column;
}

.action-buttons:first-child {
  margin-top: 0px;
}

.action-buttons {
  flex-direction: column;
  margin-top: 10px;

  border-radius: 0px;
}

.action-buttons button.action-btn.action-btn {
  border-left: 0px solid;
}

.action-buttons button.action-btn.action-btn:not(:first-child){
  border-top: 0px solid;
}

.action-buttons button.action-btn.action-btn:first-child{
  border-top-left-radius: 0px;
  border-top-right-radius: 5px;
}

.action-buttons button.action-btn.action-btn:last-child{
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 5px;
}
</style>
