<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Data</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>Data Upload</v-card-title>
      <v-card-text>
        <core-ImageUploader
          :multiple="true"
          @upload="upload"
        />

      </v-card-text>
      <v-divider/>
      <v-card-title>
        Data List
      </v-card-title>
      <v-card-text>
        <v-row dense>

          <v-col
            v-for="file in files"
            :key="file.uuid"
            cols="4"
            class="d-flex child-flex"
          >
            <v-img
              :src="`${getMediaUrl}${file.url}`"
              :lazy-src="`https://via.placeholder.com/150x100/?text=Image`"
              aspect-ratio="4/3"
              class="grey lighten-2"
              contain
            >
              <template v-slot:placeholder>
                <v-row
                  class="fill-height ma-0"
                  align="center"
                  justify="center"
                >
                  <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>
          </v-col>

          <v-col
            v-for="file in files"
            :key="file.uuid"
            :cols=4
          >

            <v-card>
              <v-card-title>File #{{file.id}}</v-card-title>
              <v-card-text>
                {{file}}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>


      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
  import DataService from '@/services/data.service';
  import { mapGetters } from 'vuex'


  export default {
    computed: {

      ...mapGetters(['getMediaUrl']),
      projectId() {
        return this.$route.params.id;
      },
    },

    data() {
      return{
        files: []
      }
    },

    created() {
      this.getFiles();
    },

    methods: {
      upload(files){
        for (const file of files)
          DataService.uploadFile(this.projectId, file)
      },

      getFiles(){
        DataService.getFiles(this.projectId)
          .then((files) => {
            this.files = files;
          })
      },
    }
  };
</script>

<style scoped></style>
