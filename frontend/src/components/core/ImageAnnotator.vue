<template>

    <div align="center">

        <core-LazyImage
          :file="file"
          thumbSize="large"
          maxHeight="675"
        >
        <div class="overlay"
          ref="overlay"
          @mouseenter="mouseEnter"
          @mousemove="mouseMove"
          @mouseleave="mouseLeave">
        </div>
      </core-LazyImage>
    </div>
</template>

<script>
export default {
  name: "ImageAnnotator",

  props: {
    file: undefined
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
    background-color: rgba(255, 0, 0, 0.3);
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
