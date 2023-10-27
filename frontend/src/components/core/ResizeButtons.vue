<template>
  <div class="overlay">
    <core-ResizeButton v-for="btn in buttons"
      :key="btn.action"
      :class="btn.action"
      :orientation="btn.orientation"
      :inverse="btn.inverse"
      @increase="$emit('increase', btn.action)"
      @decrease="$emit('decrease', btn.action)"
      />
  </div>
</template>

<script>

  class Button {
    constructor(action, orientation, inverse){
      this.action = action
      this.orientation = orientation
      this.inverse = inverse
    }
  }
  export default {
    name: "ResizeButtons",

    data: () => ({
      buttons: [
        new Button("left", "horizontal", false),
        new Button("right", "horizontal", true),
        new Button("up", "vertical", false),
        new Button("down", "vertical", true),
      ]
    })
  }
</script>


<style scoped>
  .overlay {
    background-color: rgba(255, 0, 0, 0.3);
    width: 100%;
    height: 100%;
  }


  .overlay .up, .overlay .down, .overlay .left, .overlay .right {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .overlay .up, .overlay .down {
    flex-direction: column;
    left: 0;

    height: 60px;
    width: 100%;
  }

  .overlay .up {
    top: 0px;
  }

  .overlay .down {
    bottom: 0px;
  }

  .overlay .left, .overlay .right {
    height: 100%;
    width: 60px;
    top: 0px;
    flex-direction: row;
  }

  .overlay .left {
    left: 0px;
  }

  .overlay .right {
    right: 0px;
  }


</style>
