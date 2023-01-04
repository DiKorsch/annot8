<template>
    <div class="options-bar" align="center">
      <v-card
        ref="draw_box"
        title="draw bounding box (Q)"
        @click="$emit('interaction', 'draw-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'draw-box' ? 'accent' : 'primary'">
          mdi-checkbox-blank-outline
        </v-icon>
      </v-card>

      <v-card
        ref="label_box"
        title="label bounding box (T)"
        @click="$emit('interaction', 'label-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'label-box' ? 'accent' : 'primary'">
          mdi-lead-pencil
        </v-icon>
      </v-card>

      <v-card
        ref="predict_box"
        title="predict bounding box (P)"
        @click="$emit('interaction', 'predict-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'predict-box' ? 'accent' : 'primary'">
          mdi-rocket-launch
        </v-icon>
      </v-card>

      <v-card
        ref="generate_box"
        title="generate new bounding boxes (R)"
        @click="$emit('interaction', 'generate-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'generate-box' ? 'accent' : 'primary'">
          mdi-shape-square-plus
        </v-icon>
      </v-card>

      <v-card
        ref="extreme_clicking"
        title="extreme clicking (E)"
        @click="$emit('interaction', 'extreme-clicking')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'extreme-clicking' ? 'accent' : 'primary'">
          mdi-gas-burner
        </v-icon>
      </v-card>

      <v-card
        ref="confirm_box"
        title="confirm bounding box (G)"
        @click="$emit('interaction', 'confirm-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'confirm-box' ? 'accent' : 'primary'">
          mdi-clipboard-check-multiple
        </v-icon>
      </v-card>

      <v-card
        ref="remove_box"
        title="remove bounding box (F)"
        @click="$emit('interaction', 'remove-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'remove-box' ? 'accent' : 'primary'">
          mdi-trash-can-outline
        </v-icon>
      </v-card>

      <v-card
        ref="info_box"
        title="Show info of a bounding box (I)"
        @click="$emit('interaction', 'info-box')"
        color="secondary"
        class="mt-2">
        <v-icon :color="interaction === 'info-box' ? 'accent' : 'primary'">
          mdi-information-outline
        </v-icon>
      </v-card>

    </div>
</template>

<script>
// help: https://pictogrammers.github.io/@mdi/font/6.9.96/
// option-bar from pycs
export default {
  props: {
    interaction: undefined,
  },

  created: function () {
    // subscribe to keypress events
    window.addEventListener('keypress', this.keypressEvent);
  },

  destroyed: function () {
    window.removeEventListener('keypress', this.keypressEvent)
  },

  methods: {
    keypressEvent: function (event) {
      console.log("Keyboard press");
      switch (event.key) {
        case 'q':
          this.$refs.draw_box.$el.click();
          break;
        case 'e':
          this.$refs.extreme_clicking.$el.click();
          break;
        case 't':
          this.$refs.label_box.$el.click();
          break;
        case 'p':
          this.$refs.predict_box.$el.click();
          break;
        case 'r':
          this.$refs.generate_box.$el.click();
          break;
        case 'f':
          this.$refs.remove_box.$el.click();
          break;
        case 'g':
          this.$refs.confirm_box.$el.click();
          break;
        case 'i':
          this.$refs.info_box.$el.click();
          break;
        // case 'Escape':
         // this.$emit('reset');
         // break;
      }
    },
  }
}
</script>
