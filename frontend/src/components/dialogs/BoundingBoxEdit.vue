<template>
  <v-dialog
    v-model="hasBox"
    max-width="450"
    persistent
  >
    <v-card>
      <v-card-title>
        Edit bounding box
      </v-card-title>
      <v-card-text>
        <core-CroppedImage
          :file="file"
          :box="box"
        >
          <core-ResizeButtons
            @increase="resize('increase', $event)"
            @decrease="resize('decrease', $event)"
          />
          <core-MoveButtons
            @move="move($event)"
          />
        </core-CroppedImage>
      </v-card-text>
      <v-card-actions>
        <v-col class="text-left">
          <v-btn
            color="primary"
            text
            @click="$emit('close')"
          >
            Close
          </v-btn>
        </v-col>
        <v-col class="text-right">
          <v-btn
            color="green"
            text
            @click="$emit('confirm', box)"
          >
            Update
          </v-btn>
        </v-col>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "BoundingBoxEditDialog",
  model: {prop: "box", event: "update"},

  props: {
    box: undefined,
    file: undefined,
  },

  data: () => ({
    change: 0.005,
    // localBox: {"x": undefined, "y": undefined, "width": undefined, "height": undefined},
  }),

  computed: {
    hasBox: {
      get() {
        return this.box !== undefined;
      },
      set() {
        this.$emit("close");
      }
    },
    localBox: {
      get: function() { return this.box },
      set: function(box) { this.$emit("update", box) }
    }
  },

  watch: {
    box () {
      this.copyBox()
    }
  },
  created() {
    this.copyBox()

  },

  methods: {

    copyBox(box){
      if (box === undefined)
        if (this.box === undefined)
          return
        box = this.box

      let {x, y, width, height} = box;

      this.localBox.x = x;
      this.localBox.y = y;
      this.localBox.width = width;
      this.localBox.height = height;
    },

    move(direction, change) {
      if (change === undefined)
        change = this.change;

      console.log(direction, change);
    },

    resize(action, direction, change) {
      if (change === undefined)
        change = this.change;

      if (action == "decrease")
        change = -change;

      switch(direction){
      case "left":
        this.localBox.x -= change;
        this.localBox.width += change;
        break;
      case "right":
        this.localBox.width += change;
        break;
      case "up":
        this.localBox.y -= change;
        this.localBox.height += change;
        break;
      case "down":
        this.localBox.height += change;
        break;
      default:
        console.log("Action:", action)
        console.error("Unknown direction:", direction)
        break;
      }
    },
  },
}
</script>
