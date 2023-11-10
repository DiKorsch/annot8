<template>
  <div class="move-buttons">
    <div class="move-button" :class="direction" v-for="direction in buttons" :key="direction">
    <v-tooltip
      :bottom="direction==='down'"
      :top="direction==='up'"
      :left="direction==='left'"
      :right="direction==='right'"
    >
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on"
          @click="$emit('move', direction)">
          <v-icon >
              mdi-chevron-{{direction}}
          </v-icon>
        </div>
      </template>
      <span>Move {{direction}}</span>
    </v-tooltip>
  </div>
  </div>
</template>

<script>

  export default {
    name: "MoveButtons",

    data: () => ({
      buttons: [
        "up",
        "right",
        "left",
        "down",
      ]
    })
  }
</script>


<style scoped>
  .move-buttons {
    transform: rotate(45deg);
    height: 60px;
    width: 60px;
    position: absolute;
    text-align: center;
  }

  .move-button {
    cursor: pointer;
    position: absolute;
    height: 50%;
    width: 50%;
    background: rgba(255, 255, 255, 0.1);
    transition: all 0.4s;
  }

  .move-button i {
    transform: rotate(-45deg);
    font-size: 30px;
  }

  .move-button:hover {
    background: rgba(255, 255, 255, 0.4);
  }
  .move-button.up {
    top: 0;
    left: 0;
  }
  .move-button.right {
    top: 0;
    left: 50%;
  }
  .move-button.left {
    top: 50%;
    left: 0;
  }
  .move-button.down {
    top: 50%;
    left: 50%;
  }


</style>
