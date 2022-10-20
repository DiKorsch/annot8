<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Project Creation</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>
    <v-card  outlined elevation="2" max-width=80% class="mx-auto">
      <v-card-title>New Project</v-card-title>
      <v-card-text>

        <v-container fluid>
          <v-form
            @submit.prevent="create"
            ref="form"
            >
            <v-row>
              <v-col cols=12 sm=12>
                <v-text-field
                  v-model="project.name"
                  name="name"
                  label="Project Name"
                  :error-messages="nameErrors"
                  required>
                </v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols=12 sm=12>
                <v-textarea
                  v-model="project.description"
                  name="description"
                  label="Project Description"
                  :error-messages="descErrors"
                  auto-grow
                  rows="3"
                  row-height="25"
                  required>
                </v-textarea>
              </v-col>
            </v-row>

            <v-row>
              <v-col cols=12 sm=12 class="d-flex align-end flex-column">
                <v-btn
                  type="submit"
                  color="primary"
                >
                  Create
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
      </v-card-text>
    </v-card>

  </v-container>
</template>

<script>
  import Project from '@/store/models/project';
  import DataService from '@/services/data.service';
  import { validationMixin } from 'vuelidate';
  import { required, minLength } from 'vuelidate/lib/validators';
  import { mapState } from 'vuex'

  export default {
    name: 'CreateProject',

    mixins: [validationMixin],

    validations: {
      project: {
        name: { required, minLength: minLength(3) },
        description: { required },
      }
    },

    data () {
      return {
        project: new Project(),
      }
    },

    computed: {
      nameErrors () {
        const errors = [];
        if (!this.$v.project.name.$dirty) return errors
        !this.$v.project.name.minLength && errors.push('Name must be at least 3 characters long')
        !this.$v.project.name.required && errors.push('Name is required')
        return errors;
      },

      descErrors () {
        const errors = [];
        if (!this.$v.project.description.$dirty) return errors
        !this.$v.project.description.required && errors.push('Description is required')
        return errors;
      },

      modelErrors () {
        const errors = [];
        if (!this.$v.project.model.$dirty) return errors
        !this.$v.project.model.required && errors.push('Please select a model.')
        return errors;
      },

      labelProviderErrors () {
        const errors = [];
        if (!this.$v.project.labelProvider.$dirty) return errors
        return errors;
      },

      ...mapState(['data'])
    },

    methods: {
      create() {
        this.$v.$touch();

        if (this.$v.$invalid)
          return

        DataService.project.create(this.project).then(
          (project) => {
            this.$router.push({ name: 'project', params: { id: project.id}})
        })
      }
    },

    created () {
    },
  }
</script>

<style scoped>

</style>
