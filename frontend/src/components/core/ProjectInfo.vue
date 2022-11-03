<template>
  <v-col :cols="cols">
    <v-card
      outlined
      :elevation="selected ? 10 : 2"
      class="mx-auto"
      @click="select"
      >
      <v-card-title>Name: {{project.name}}</v-card-title>
      <v-card-text>
          <p>Desc: {{project.description}}</p>
          <!-- <p>Root: {{projec.rootFolder}}</p> -->
          <p>UUID: {{project.uuid}}</p>
      </v-card-text>
      <v-card-actions v-if="selected" align="right">
        <v-list-item class="grow">
          <v-row align="center" justify="end">
            <v-btn text
              v-for="(action, index) in actions" :key="index"
              color="primary"
              :to="{name: action.dest, params: {id: project.id}}"
            >
               <v-icon left>{{action.icon}}</v-icon>
               {{action.text}}
            </v-btn>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </v-col>
</template>


<script>
import Project from "@/store/models/project"

class Action {
  constructor(text, icon, dest){
    this.text = text;
    this.icon = icon;
    this.dest = dest;
  }
}

export default {
  name: "ProjectInfo",

  data: () => ({
    selected: false,
  }),

  computed: {

    actions: () => ([
      new Action(
        "Options", "mdi-cog", "project"),
      new Action(
        "Data", "mdi-image-multiple", "data"),
      new Action(
        "Labels", "mdi-label-multiple", "labels"),
      new Action(
        "Annotate", "mdi-pencil", "annotations"),
    ])
  },

  props: {
    project: {
      type: Project,
      default: new Project(),
    },
    cols: {
      type: Number,
      default: 12,
    },
  },

  methods: {
    select: function(){
      // this way, we can toggle between selected and unselected
      var arg = this.selected ? undefined : this.project.id;
      this.$emit('selected', arg);

    }
  }
}
</script>

<style scoped>

</style>
