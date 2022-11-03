<template>
  <div class="overlay">
    <core-LazyImage
      :file="file"
      thumbSize="large"
      maxHeight="675"
      />
  <!--
    <v-row>
      <v-col :cols=12>
      </v-col>
      <v-col :cols=2>
        <v-card>
          <v-card-text>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
          tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
          quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
          consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
          cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
          proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</v-card-text>
        </v-card>
      </v-col>
    </v-row>
    -->
  </div>



</template>

<script>
export default {
  name: "ImageAnnotator",

  props: {
    file: undefined
  }
}
</script>
