<template>
  <div class="bounding-box" :style="style">
    <v-chip label x-small color="primary">
      {{ localValue.label }}
    </v-chip>
  </div>
</template>

<script>

export default {
  name: "BoundingBox",
  model: {prop: "value", event: "input"},

  props: {
    value: undefined
  },

  computed: {
    localValue: {
      get: function(){ return this.value },
      set: function(value){ this.$emit('input', value) },
    },

    style: function() {
      return {
        top: `${this.value.y * 100}%`,
        left: `${this.value.x * 100}%`,
        width: `${this.value.w * 100}%`,
        height: `${this.value.h * 100}%`,
      }
    }
  },

}

</script>


<style scoped>
  .bounding-box{
    position: absolute;

    background-color: rgba(0, 0, 255.0, 0.3);
    color: whitesmoke;
  }

  .bounding-box:hover{
    background-color: rgba(0, 0, 255.0, 0.4);

  }
</style>
