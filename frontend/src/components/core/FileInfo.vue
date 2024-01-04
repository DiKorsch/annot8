<template>
<div style="border-style: 1px solid;">

  <v-card>
    <core-LazyImage :file="file" thumbSize="medium"/>
    <v-card-title>{{file.name}}</v-card-title>
    <!-- <v-card-text>
      {{file}}
    </v-card-text> -->
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn small
        color="primary"
        :to="{name: 'annotate', params: {fileId: file.id}}"
      >
        <v-icon>mdi-tag</v-icon>
      </v-btn>
      <v-btn small
        color="error"
        @click="$emit('delete', file)"
      >
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</div>
</template>

<script>

export default {
  name: "FileInfo",
  props: {
    file: undefined,
    bboxes: undefined,
  },

}
</script>


<style scoped>
  .info-overlay {

  }
</style>
