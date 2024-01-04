<template>
  <v-bottom-sheet
    inset
    v-model="isOpen"
  >
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
  model: {prop: "dialog", event: "opened"},

  props: {
    dialog: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
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

  computed: {
    isOpen: {
      get() { return this.dialog },
      set(val) { this.$emit("opened", val) },
    }
  },

  created() {
    this.getLabels();
  },
}
</script>
