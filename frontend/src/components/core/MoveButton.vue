<template>
  <div >
    foo
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
