<template>
  <div class="overlay">
    <div v-for="direction in buttons"
      :key="direction"
      :class="direction"
      @click="$emit('move', direction)">
      <v-icon >
          mdi-chevron-{{direction}}
      </v-icon>
    </div>
  </div>
</template>

<script>

  export default {
    name: "MoveButtons",

    data: () => ({
      buttons: [
        "left",
        "right",
        "up",
        "down",
      ]
    })
  }
</script>


<style scoped>
  .overlay {
    width: 60px;
    height: 60px;
  }

  .overlay .up, .overlay .down, .overlay .left, .overlay .right {
    cursor: pointer;
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 0, 0, 0.2);

    height: 30px;
    width: 30px;
  }
  .overlay .up:hover, .overlay .down:hover, .overlay .left:hover, .overlay .right:hover {
    background-color: rgba(255, 0, 0, 0.4);
  }

  .overlay .up, .overlay .down {
    flex-direction: column;
    left: 50%;
  }

  .overlay .up {
    bottom: 50%;
  }

  .overlay .down {
    top: 50%;
  }

  .overlay .left, .overlay .right {
    top: 50%;
    flex-direction: row;
  }

  .overlay .left {
    right: 50%;
  }

  .overlay .right {
    left: 50%;
  }


</style>
