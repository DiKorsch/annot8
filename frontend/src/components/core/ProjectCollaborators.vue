<template>
  <v-row>
   <v-col class="col-8">
    <div v-if="project.collaborators.length">
      <v-row>
        <v-chip
          cols=6
          v-for="(user, i) in project.collaborators"
          :key="i"
          close
          close-icon="mdi-close"
          outlined
          @click:close="removeCollab(user)"
        >
          <v-avatar left>
            <v-icon>mdi-account-circle</v-icon>
          </v-avatar>
          {{ user }}
        </v-chip>
      </v-row>
    </div>

    <div v-else>None</div>
   </v-col>
   <v-col class="col-4" align="right">
    <v-tooltip top>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          small dark
          color="primary"
          elevation="2"
          v-on="on"
          v-bind="attrs"
          @click="dialog = true"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
      <span>Add new collaborator</span>
    </v-tooltip>

    <v-dialog
      v-model="dialog"
      width="500">

      <v-card>
        <v-card-title class="grey lighten-2">
         Enter the name of the user you want to add
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-text-field
              label="Username"
              v-model="name_to_add"
              solo
            ></v-text-field>

            <v-alert v-if="error !== undefined"
              type="error"
              outlined
              dense
              border="left"
            >
              {{ this.error }}
            </v-alert>
          </v-container>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="addCollab">
            Add Collaborator
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
   </v-col>
  </v-row>
</template>


<script>
import DataService from '@/services/data.service';

export default {
  name: "ProjectCollaborators",
  data: () => ({
    dialog: false,
    name_to_add: undefined,

    error: undefined,
  }),

  props: {
    project: undefined,
  },

  methods: {
    removeCollab: function (user) {
      console.log(`Removing ${user}`)
      this.error = undefined;
      DataService.collaborator.remove(this.project.id, user)
        .then((ok) => {
          if (!ok){
            this.error = "Collaborator could not be added. \
            Please check whether the username is spelled correctly. \
            Also, make sure that the user is not already a collaborator or \
            creator of the project!";
            return;
          }
          this.$router.go(); // reload current view
        });
    },

    addCollab: function() {
      console.log(`Adding ${this.name_to_add}`)
      this.error = undefined;
      DataService.collaborator.add(this.project.id, this.name_to_add)
        .then((ok) => {
          if (!ok){
            this.error = "Collaborator could not be added. \
            Please check whether the username is spelled correctly. \
            Also, make sure that the user is not already a collaborator or \
            creator of the project!";
            return;
          }
          this.$router.go(); // reload current view
        });

    }
  },


}
</script>
