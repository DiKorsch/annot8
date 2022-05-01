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

  export default {
    name: 'LoginView',

    data () {
      return {
        valid: false,
        user: new User('', ''),
        loading: false,
        incorrectAuth: false,
        showPwd: false,
        rules: {
          required: [value => !!value || 'Required.'],
        },
      }
    },

    computed: {
      loginErrors () {
        const errors = []
        this.incorrectAuth && errors.push('Username or password are incorrect.')
        return errors
      },
      loggedIn() {
        return this.$store.state.auth.loggedIn;
      }
    },
    created() {
      if (this.loggedIn){
        this.$router.push({ name: 'index' })
      }
    },


    methods: {
      login () {
        this.loading = true;

        this.$store.dispatch('auth/login', this.user).then(
          () => {
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
