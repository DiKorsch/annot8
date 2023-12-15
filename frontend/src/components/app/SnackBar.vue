<template>
    <v-snackbar
      v-if="message !== undefined"
      v-model="snackbar"
      outlined
      :timeout="message.timeout"
    >
      {{ message.content }}
      <template v-slot:action="{ attrs }">
        <v-btn
          icon
          text
          v-bind="attrs"
          @click="message = undefined"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
</template>

<script>
// import { mapGetters } from 'vuex'
export default {
  name: "SnackBar",
  data: () => ({
    message: undefined,
    timeout: -1,
  }),

  created() {
    this.$store.dispatch("messages/register", this);
  },

  computed: {
    snackbar: {
      get(){
        return this.message !== undefined
      },
      set(){
        this.message = undefined
      },
    }
  },

  methods: {
    // ...mapGetters("messages", ["nextMessage"]),

    newMessage(msg){
      console.log("[SnackBar] new message arrived: ", msg)
      this.message = msg;
    }
  }

}
</script>
