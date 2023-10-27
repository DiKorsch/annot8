<template>
  <div v-if="inverse" class="resize-button-container">
      <div class="resize-button" @click="$emit('increase')">
        <v-icon>mdi-{{incIcon}}</v-icon>
      </div>
      <div class="resize-button" @click="$emit('decrease')">
        <v-icon>mdi-{{decIcon}}</v-icon>
      </div>
  </div>
  <div v-else class="resize-button-container">
      <div class="resize-button" @click="$emit('decrease')">
        <v-icon>mdi-{{decIcon}}</v-icon>
      </div>
      <div class="resize-button" @click="$emit('increase')">
        <v-icon>mdi-{{incIcon}}</v-icon>
      </div>
  </div>
</template>

<script>

  export default {
    name: "ResizeButton",

    data: () => ({
    }),

    props: {
      orientation: undefined,
      inverse: {
        type: Boolean,
        default: false
      }
    },

    computed: {
      incIcon(){
        if (this.orientation == "vertical")
          return this.inverse ? "chevron-up" : "chevron-down"
        else
          return this.inverse ? "chevron-right" : "chevron-left"
      },
      decIcon(){
        if (this.orientation == "vertical")
          return this.inverse ? "chevron-down" : "chevron-up"
        else
          return this.inverse ? "chevron-left" : "chevron-right"
      },
    }
  }
</script>


<style scoped>
  .resize-button-container {
    position: absolute;
/*    background-color: rgba(0, 0, 255, 0.3);*/
  }

  .resize-button {
    cursor: pointer;
    width: 100%;
    height: 100%;

    display: inherit;
    justify-content: inherit;
    align-items: inherit;

  }
  .resize-button:hover {
    background-color: rgba(255, 255, 255, .3);
  }
</style>
