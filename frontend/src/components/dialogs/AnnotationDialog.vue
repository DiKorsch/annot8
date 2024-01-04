<template>
  <v-bottom-sheet
    v-model="dialog"
    inset
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        v-on="on"
        small
      >
        <v-icon>mdi-tag</v-icon> Annotate
      </v-btn>
    </template>
    <core-LabelList
      :labels="labels"
      :parent="$route.query.parent"
      :selectable="true"
      @selected="$emit('selected', $event)"
    />
  </v-bottom-sheet>
</template>

<script>
import DataService from '@/services/data.service';

export default {
  name: "AnnotationDialog",

  data: () => ({
    dialog: false,
    labels: [],
  }),

  methods: {

    getLabels(){
      DataService.labels.get()
        .then((labels) => {
          this.labels = labels;
        })
    },

    select(label) {
      console.log("[Annotation dialog] selected", label)
    }
  },
  created() {
    this.getLabels();
  },
}
</script>
