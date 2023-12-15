<template>
    <v-snackbar
      v-if="message !== undefined"
      :color="message.level"
      v-model="snackbar"
      :timeout="-1"
    >
    <v-row class="d-flex align-center">
      <v-col cols=auto><v-icon>mdi-{{icon}}</v-icon></v-col>
      <v-col>{{ message.content }}</v-col>
      <v-col cols=auto>
        <v-progress-circular
          :value="remainingTime"
        >
          <v-btn
            icon
            text
            @click="message = undefined"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-progress-circular>

      </v-col>
    </v-row>

    </v-snackbar>
</template>

<script>
export default {
  name: "SnackBar",
  data: () => ({
    message: undefined,
    remainingTime: 100,
  }),

  created() {
    this.$store.dispatch("messages/register", this);
  },

  computed: {
    icon() {
      return {
        info: "information-outline",
        alert: "alert-circle-outline",
        error: "close-octagon",
      }[this.message?.level] || "cross";
    },

    snackbar: {
      get(){
        return this.message !== undefined
      },
      set(){
        this.message = undefined;
        this.messageTime = undefined;
      },
    },
  },

  methods: {

    decreaseTimer(duration, step=100){
      if(duration === -1)
        return;
      // let t0 = this.remainingTime;
      this.remainingTime -= 100 * (step / duration)
      // let t1 = this.remainingTime;

      // console.log(t0, "->", t1, step / duration)

      if (this.remainingTime > 0)
        setTimeout(this.decreaseTimer, step, duration, step)
      else
        setTimeout(this.newMessage, 500) // this will delete current message
    },

    newMessage(msg){
      this.message = msg;
      if (this.message === undefined)
        return;

      console.log("[SnackBar] new message arrived: ", msg)
      this.remainingTime = 100;
      this.decreaseTimer(msg.timeout)
    }
  }

}
</script>
