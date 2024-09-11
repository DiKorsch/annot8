<template>
  <v-container fluid>
    <h1>Index Page</h1>

    <v-card v-if="loggedIn">
      <v-card-title>
        Logged in as {{ username }}
      </v-card-title>
      <v-card-text>
        Check out following links:
        <v-row>
          <v-col cols="auto">
            <v-btn :to = "{ name: 'projects' }" color="primary">Your Projects</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn :to = "{ name: 'labels' }">Label list</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn :to = "{ name: 'change_password' }" color="error">Change password</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-container>
</template>


<script>
import { mapGetters } from 'vuex'

export default {
  name: 'IndexView',

  computed: {
    ...mapGetters("auth", ["loggedIn", "username"]),
  },
}
</script>
