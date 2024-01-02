<template>
  <v-row class="view-header">
    <v-col cols=6>
      <h1>{{title}}</h1>
    </v-col>
    <v-col cols=4><slot></slot></v-col>
    <v-col cols=2 >
      <v-btn v-if="dest !== undefined" :to = "{ name: dest }" block :color="color">
        <v-icon>{{icon}}</v-icon> {{text}}
      </v-btn>
    </v-col>
  </v-row>
</template>


<script>
export default {
  name: "AppHeader",
  data: () => ({
  }),
  props: {
    title: {
      type: String,
      default: "APP"
    },
    dest: undefined,
    text: {
      type: String,
      default: "Projects"
    },
    color: {
      type: String,
      default: "primary"
    },
    icon: {
      type: String,
      default: "mdi-book-multiple"
    },

  }
}
</script>
