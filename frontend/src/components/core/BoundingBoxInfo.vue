<template>
  <v-list-item dense class="bbox-info">
    <v-list-item-content class="label">
      <v-list-item-title>{{this.label}}</v-list-item-title>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn-toggle dense borderless>
        <v-icon
          small
          class="info-button"
          @click="$emit('select', bbox.id)">mdi-magnify
        </v-icon>
      <v-icon
        small
        class="info-button"
        @click="$emit('toggle', bbox.id)">mdi-eye-outline
      </v-icon>
      <v-icon
        small
        class="info-button"
        @click="$emit('remove', bbox.id)">mdi-trash-can-outline
      </v-icon>
      </v-btn-toggle>
    </v-list-item-action>
  </v-list-item>
</template>


<script>
export default {
  name: "BoundingBoxInfo",

  props: {
    bbox: undefined
  },
  computed: {
    label: function() {

      if (this.bbox.label !== null) {
        return this.bbox.label
      } else
      return `#${this.bbox.id}`
    }
  }
}
</script>


<style scoped>
.bbox-info {
  background-color: red;
}
.bbox-info .info-button {
  margin: 2px 5px;
}
.bbox-info .label {
  font-size: smaller;
}
</style>
