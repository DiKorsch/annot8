<template>
  <v-hover>
    <template v-slot:default="{ hover }">
      <core-LazyImage :file="file" thumbSize="medium">
        <v-fade-transition>
          <v-overlay
            v-if="hover"
            absolute
            color="grey darken-4"
          >
          <v-card class="info-overlay" overline width="100%">
            <v-card-subtitle>
              <v-row dense class="text-caption">
                <v-col cosl=12 class="text-truncate">{{file.name}}</v-col>
              </v-row>
            </v-card-subtitle>
            <v-card-text>
              <div v-if="file.meta !== undefined">
                <v-row dense class="text-caption" v-for="info, i in file.meta" :key="i">
                  <v-col cols=6 class="text-right">{{info[0]}}</v-col>
                  <v-col cols=6 class="text-left">{{info[1]}}</v-col>
                </v-row>
              </div>
            </v-card-text>

            <div v-if="hasButtons">

              <v-divider></v-divider>

              <v-card-actions>
                <v-btn v-if="annotateButton" small
                  color="success"
                  :to="{name: 'annotate', params: {fileId: file.id}}"
                >
                  <v-icon>mdi-tag</v-icon>
                </v-btn>
                <v-spacer/>
                <v-btn v-if="deleteButton" small
                  color="error"
                  @click="$emit('delete', file)"
                >
                  <v-icon>mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-card-actions>
            </div>
          </v-card>
          </v-overlay>
        </v-fade-transition>
      </core-LazyImage>
    </template>
  </v-hover>
</template>

<script>

export default {
  name: "FileInfo",
  props: {
    file: undefined,
    bboxes: undefined,

    annotateButton: {
      type: Boolean,
      default: true
    },
    deleteButton: {
      type: Boolean,
      default: true
    },
  },

  computed: {
    hasButtons() {
      return this.annotateButton || this.deleteButton
    }
  }

}
</script>


<style>
  .v-overlay__content:has(.info-overlay) {
    width: 90%;
  }
</style>
