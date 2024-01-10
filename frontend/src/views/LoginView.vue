<template>
  <v-card shaped outlined elevation="2" max-width=600px class="mx-auto">
    <v-card-title>Login</v-card-title>
    <v-card-text>
      <v-form
        @submit.prevent="login"
        v-model="valid"
        ref="form"
        >
        <v-container fluid>
          <v-row>
            <v-col cols=12 sm=12>
              <v-text-field
                v-model="user.username"
                name="username"
                label="Username"
                :rules="rules.required"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols=12 sm=12>
              <v-text-field
                v-model="user.password"
                :append-icon="showPwd ? 'mdi-eye' : 'mdi-eye-off'"
                name="password"
                label="Password"
                :rules="rules.required"
                :type="showPwd ? 'text' : 'password'"
                :error-messages="loginErrors"
                @click:append="showPwd = !showPwd"
                required
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols=12 sm=12>
              <v-btn
                class="mr-4"
                type="submit"
              >
                Login
              </v-btn>
            </v-col>
          </v-row>

        </v-container>

      </v-form>

    </v-card-text>
  </v-card>
</template>

<script>
import User from '@/store/models/user';
import DataService from '@/services/data.service';
import { mapGetters } from 'vuex'

export default {
  name: 'LoginView',

  data: () => ({
      valid: false,
      user: new User('', ''),
      loading: false,
      incorrectAuth: false,
      showPwd: false,
      rules: {
        required: [value => !!value || 'Required.'],
      },
  }),


  computed: {
    ...mapGetters("auth", ["loggedIn"]),

    loginErrors () {
      const errors = []
      if (this.incorrectAuth)
        errors.push('Username or password are incorrect.')
      return errors
    },

    next() {
      return this.$route.query["next"]
    }

  },
  created() {
    if (this.loggedIn)
      this.$router.push({ name: 'index' })

    console.log("[Login] redirecting to", this.next)
  },


  methods: {
    login () {
      this.loading = true;

      this.$store.dispatch('auth/login', this.user).then(
        () => {
          DataService.initData();
          this.$router.push({ name: 'index' })
        },
        err => {
          console.log(err)
          this.incorrectAuth = true
        }
      )
    }
  }
}
</script>


<style scoped>
  .login{
    background-color: #fff;
    margin-top: 10%;
  }

  input {
    padding: 25px 10px;
  }
</style>
