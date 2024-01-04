<template>
  <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          :color="color"
          v-bind="attrs"
          v-on="on"
          x-small
          @click="$emit('click')"
        >
          <slot></slot>
        </v-btn>
      </template>
      <span>{{tooltip}}</span>
    </v-tooltip>
</template>

<script >
export default {
  name: "ConfirmButton",
  props: {
    tooltip: {
      type: String,
      default: "Tooltip"
    },
    color: {
      type: String,
      default: "primary"
    },
  }
}
</script>
