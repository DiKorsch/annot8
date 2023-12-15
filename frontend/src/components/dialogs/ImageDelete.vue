<template>
  <v-dialog
    v-model="model"
    max-width="500px"
  >
    <v-card>
      <core-LazyImage :file="file" />
      <v-card-title class="grey lighten-2">
        Do you wish to delete file
        <span class="mx-1" v-if="file !== undefined">
          <b>{{ file.name }}</b>
        </span>?
      </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="$emit('close')">No</v-btn>
        <v-btn @click="$emit('confirm', file)" color="error">Yes</v-btn>
      </v-card-actions>
    </v-card>

    <utils-KeypressHandler @pressed="handleKeyPress($event)"/>
  </v-dialog>
</template>

<script>

export default {
  name: "ImageDeleteDialog",

  props: {
    file: undefined,
  },

  methods: {
    handleKeyPress(event){
      if (event.key == "Enter")
        this.$emit("confirm", this.file)
    }
  },


  computed: {
    model: {
      get() {
        return this.file !== undefined;
      },
      set() {
        this.$emit("close");
      }
    }
  }
}

</script>
