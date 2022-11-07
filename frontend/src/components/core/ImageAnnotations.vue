<template>
  <div class="overlay"
    ref="overlay"
    @mouseenter="mouseEnter"
    @mousemove="mouseMove"
    @mouseleave="mouseLeave"
  >
    <v-chip small label>{{annotations.label}}</v-chip>
    <core-BoundingBox
      v-for="(box, i) in annotations.boxes"
      :value="box"
      :key="i"
    />
  </div>
</template>


<script>

export default {
  name: "ImageAnnotations",

  props: {
    annotations: []
  },

  methods: {

    mouseEnter() {
      console.log('mouseenter');
      // this.$el.addEventListener('mousemove', this.mouseMove, false);
    },
    mouseLeave() {
      console.log('mouseleave');
      // this.$el.removeEventListener('mousemove', this.mouseMove());
    },
    mouseMove(event) {
      console.info(event.layerX, event.layerY);
    }
  }

}
</script>

<style scoped>
  .overlay{
    /*background-color: rgba(255, 0, 0, 0.3);*/
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>

