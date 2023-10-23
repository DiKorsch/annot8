<template>
  <v-dialog
    v-model="hasBox"
    max-width="500px"
  >
    <v-card>
      <v-card-title>
        Do you really want to delete this box?
      </v-card-title>
      <v-card-text>
        {{ box }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          color="red"
          align="left"
          text
          @click="$emit('confirm', box)"
        >
          Yes, delete it.
        </v-btn>

        <v-btn
          color="primary"
          text
          @click="$emit('close')"
        >
          No, close this window
        </v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "BoundingBoxDeleteDialog",

  props: {
    box: undefined
  },

  computed: {
    hasBox: {
      get() {
        return this.box !== undefined;
      },
      set() {
        this.$emit("close");
      }
    }
  }
}
</script>
