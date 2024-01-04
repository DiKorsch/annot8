<template>
  <v-dialog
    v-model="model"
    max-width="500px"
  >
    <v-card>
      <v-card-title>
        Do you really want to delete this file?
      </v-card-title>
      <v-card-subtitle>
        Attention: this cannot be undone!
      </v-card-subtitle>
      <v-card-text>
        <core-FileInfo :file="file"
          :annotateButton="false"
          :deleteButton="false"
        />
      </v-card-text>
      <v-card-actions>

        <v-col class="text-left">
          <v-btn
            color="primary"
            text
            @click="$emit('close')"
          >
            No, close this window
          </v-btn>
        </v-col>

        <v-col class="text-right">
          <v-btn
            color="red"
            align="left"
            text
            @click="$emit('confirm', file)"
          >
            Yes, delete it.
          </v-btn>
        </v-col>
      </v-card-actions>
    </v-card>

    <utils-KeypressHandler v-if="handleKeys" @pressed="handleKeyPress($event)"/>
  </v-dialog>
</template>

<script>

export default {
  name: "ImageDeleteDialog",

  props: {
    file: undefined,

    handleKeys: {
      type: Boolean,
      default: true,
    }
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
