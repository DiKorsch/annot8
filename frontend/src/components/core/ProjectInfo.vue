<template>
  <v-col :cols="cols">
    <v-card
      outlined
      elevation="2"
      class="mx-auto"
      >
      <v-card-title>{{project.name}}</v-card-title>
      <v-card-subtitle>{{project.description}}</v-card-subtitle>
      <v-card-text>
        <v-row dense>
          <v-col cols=6>
            <v-row>
              <v-col>
                 Uploaded Files
              </v-col>
              <v-col align="right">
                <v-chip small>{{project.stats.nFiles}}</v-chip>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                 Annotated boxes
              </v-col>
              <v-col align="right">
                <v-chip small>{{project.stats.nBoxes}}</v-chip>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols=6 align="right">
            <v-btn-toggle>
              <v-tooltip
                v-for="(action, index) in actions"
                :key="index"
                top
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    :to="{name: action.dest, params: {id: project.id}}"
                    v-bind="attrs"
                    v-on="on"
                  >
                     <v-icon center>{{action.icon}}</v-icon>
                  </v-btn>
                </template>

                <span>{{action.text}}</span>
              </v-tooltip>
            </v-btn-toggle>
          </v-col>
        </v-row>
      </v-card-text>
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
        "Manage Data", "mdi-image-multiple-outline", "data"),
      new Action(
        "Annotate Images", "mdi-image-multiple", "annotations"),
      new Action(
        "Annotate Crops", "mdi-checkbox-multiple-blank-outline", "crops"),
      new Action(
        "Settings", "mdi-cog", "project"),
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
}
</script>

<style scoped>

</style>
