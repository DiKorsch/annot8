<template>
  <div v-if="inverse" class="resize-button-container">
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on" class="resize-button" @click="$emit('decrease')">
          <v-icon>mdi-chevron-{{decIcon}}</v-icon>
        </div>
      </template>
      <span>Shrink</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on" class="resize-button" @click="$emit('increase')">
      <v-icon>mdi-chevron-{{incIcon}}</v-icon>
    </div>
      </template>
      <span>Enlarge</span>
    </v-tooltip>
  </div>
  <div v-else class="resize-button-container">
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on" class="resize-button" @click="$emit('increase')">
      <v-icon>mdi-chevron-{{incIcon}}</v-icon>
    </div>
      </template>
      <span>Enlarge</span>
    </v-tooltip>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on" class="resize-button" @click="$emit('decrease')">
          <v-icon>mdi-chevron-{{decIcon}}</v-icon>
        </div>
      </template>
      <span>Shrink</span>
    </v-tooltip>
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
          return this.inverse ? "down" : "up"
        else
          return this.inverse ? "right" : "left"
      },
      decIcon(){
        if (this.orientation == "vertical")
          return this.inverse ? "up" : "down"
        else
          return this.inverse ? "left" : "right"
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

    background-color: rgba(255, 255, 255, .2);
  }
  .resize-button:hover {
    background-color: rgba(255, 255, 255, .4);
  }
</style>
