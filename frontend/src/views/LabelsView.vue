<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Labels</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>

    <core-LabelList
      :labels="labels"
      :parent="$route.query.parent"
    />

  </v-container>
</template>

<script>
import DataService from '@/services/data.service';

export default {
  data: () => ({
    labels: [],
  }),

  methods: {

    getFiles(){
      DataService.labels.get()
        .then((labels) => {
          this.labels = labels;
        })
    },
  },
  created() {
    this.getFiles();
  },

}
</script>
