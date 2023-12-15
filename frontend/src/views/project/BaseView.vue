<template>
  <router-view/>
</template>


<script>
export default{
  name: "BaseProjectView",

  created: function() {
    console.log("BASE PROJECT VIEW CREATED!", this.$route.params.id)
  }
}
</script>
