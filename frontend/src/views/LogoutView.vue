<template>
  <div class="log">
  </div>
</template>

<script>
  export default {
    created () {
      this.$store.dispatch('auth/logout')
        .then(() => {
          this.$router.push({ name: 'login' })
        })
    }
  }
</script>

<style>
</style>
