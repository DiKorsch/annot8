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
      <v-card-actions v-if="selected" class="justify-center">
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
        "Manage Data", "mdi-image-multiple-outline", "data"),
      new Action(
        "Annotate Images", "mdi-image-multiple", "annotations"),
      new Action(
        "Annotate Crops", "mdi-checkbox-multiple-blank-outline", "crops"),
      new Action(
        "Show Labels", "mdi-label-multiple", "labels"),
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
