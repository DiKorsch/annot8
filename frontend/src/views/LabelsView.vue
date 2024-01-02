<template>
  <v-container fluid>
    <app-ViewHeader title="Labels"/>
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
