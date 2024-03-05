<template>
  <div></div>
</template>

<script>
export default {
  name: "KeypressHandler",

  created: function () {
    // subscribe to keypress events
    window.addEventListener('keydown', this.keypressEvent);
  },

  destroyed: function () {
    window.removeEventListener('keydown', this.keypressEvent)
  },

  methods: {

    keypressEvent: function (event) {
      console.debug("[KeypressHandler] Keyboard press:", event.key, event);
      this.$emit("pressed", event)
    }
  }
}
</script>
