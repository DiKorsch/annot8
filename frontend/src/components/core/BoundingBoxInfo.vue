<template>
  <div>

  <v-img
    :src="thumb"
    contain
    :max-height="maxHeight"
    position="center center"
  />
  <v-row v-if="predicted_label">
    <v-col class="header" cols=4>Predicted label</v-col>
    <v-col cols=5><a :href="gbif_link(bbox.predicted_label)" target="_new">{{predicted_label}}</a></v-col>
    <v-col cols=3>
      <utils-ConfirmButton
        color="green lighten-2"
        @click="confirm(bbox, true)"
      >
        <v-icon color="white">mdi-check</v-icon>
      </utils-ConfirmButton>
    </v-col>
  </v-row>
  <v-row v-else>
    <v-col cols=12>
      <v-btn small @click="$emit('predict', bbox)"><v-icon>mdi-brain</v-icon> Predict</v-btn></v-col>
  </v-row>


  <v-row v-if="annotated_label">
    <v-col class="header" cols=4>Annotated label</v-col>
    <v-col cols=5><a :href="gbif_link(bbox.label)" target="_new">{{annotated_label}}</a></v-col>
    <v-col cols=3>
      <utils-ConfirmButton
        color="green lighten-2"
        @click="confirm(bbox, false)"
      >
        <v-icon color="white">mdi-check</v-icon>
      </utils-ConfirmButton>
    </v-col>
  </v-row>
  <v-row v-else>
    <v-col cols=12>
      <v-btn small @click="$emit('annotate')">
        <v-icon>mdi-tag</v-icon> Annotate
      </v-btn>
    </v-col>
  </v-row>

  <v-row v-if="bbox.annotator">
    <v-col class="header" cols=4>Annotated by</v-col>
    <v-col cols=5>{{bbox.annotator}}</v-col>
  </v-row>
  <v-row v-if="bbox.confirmators">
    <v-col class="header" cols=4>Confirmed by</v-col>
    <v-col cols=5>{{bbox.confirmators}}</v-col>
  </v-row>
  </div>

</template>


<script>
import { mapGetters } from 'vuex';

export default {
  name: "BoundingBoxInfo",

  props: {
    bbox: undefined,
    maxHeight: undefined,
  },

  data: () => ({
    thumbSize: "original"
  }),

  computed: {
    ...mapGetters(['getMediaUrl']),

    label: function() {
      return this.bbox.label || this.bbox.predicted_label;
    },
    predicted_label: function() {
      return this.bbox.predicted_label?.name;
    },
    annotated_label: function() {
      return this.bbox.label?.name;
    },
    hasLabel: function(){
      let lab = this.label;
      return lab !== undefined && lab !== null ;
    },
    thumb: function() {

      let boxThumbs = this.bbox?.crops;
      let url = ""
      if (boxThumbs !== undefined && boxThumbs[this.thumbSize] !== undefined )
        url = boxThumbs[this.thumbSize]

      return `${this.getMediaUrl}${url}`
    },

  },
  methods: {
    gbif_link(label){
      return `https://www.gbif.org/occurrence/gallery?media_type=StillImage&life_stage=Imago&taxon_key=${label.id}`
    },

    confirm(bbox, is_predicted){
      if(is_predicted)
        console.log("Confirming predicted label", bbox.predicted_label)
      else
        console.log("Confirming annotated label", bbox.label)
    }
  }
}
</script>


<style scoped>
.bbox-info {
  padding: 3px;
}

.bbox-info.selected {
  background-color: rgba(0, 0, 0, 0.1);
  border-style: solid;
  border-width: 1px;
  padding: 2px;
}
.bbox-info .info-button {
  margin: 2px 5px;
}
.bbox-info .label {
  font-size: smaller;
  flex-wrap: nowrap;
  padding: 0px 0px;
}

.header {
  text-align: left;
  font-weight: bold;
}
</style>
