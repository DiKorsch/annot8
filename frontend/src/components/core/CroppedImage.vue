<template>
  <div @click="$emit('click')">
    <v-row v-if="qualitySelector">
      <v-col>Quality:</v-col>
      <v-col class="text-right">
        <v-btn-toggle
            v-model="thumbSize"
            color="deep-purple accent-3"
            group
            dense
            mandatory
          >
          <v-btn
            v-for="size in thumbSizes"
            :key="size.key"
            :value="size.key"
            x-small
            >
              {{size.text}}
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div class="cropped-img">
          <v-tooltip top v-if="hasLabel">

            <template v-slot:activator="{ on, attrs }">
              <div
                v-bind="attrs"
                v-on="on"
                class="label lighten-1"
                :class="{
                  blue: box.label !== null,
                  green: box.label === null,
                }"
                >
                <v-icon small v-if="box.label !== null">mdi-tag</v-icon>
                <v-icon small v-else>mdi-brain</v-icon>
              </div>
            </template>
            <span>{{label}}</span>
          </v-tooltip>
          <img ref="image" :src="src" :style="style">
          <slot></slot>
        </div>
      </v-col>
    </v-row>
  </div>

</template>


<script>
import { mapGetters } from 'vuex';
export default {
  name: "CroppedImage",

  props: {
    file: undefined,
    box: undefined,
    useThumbs: {
      type: Boolean,
      default: true,
    },
    initialThumbSize: {
      type: String,
      default: "large"
    },
    qualitySelector: {
      type: Boolean,
      default: true
    }
  },

  data: () => ({
    pad: 0.00,
    // imgSize: undefined,
    thumbSize: undefined,
    thumbSizes: [
      {key: "small", text: "Low"},
      {key: "medium", text: "Medium"},
      {key: "large", text: "High"},
      {key: "original", text: "Original"},
    ],
  }),

  created() {

    this.thumbSize = this.initialThumbSize;
  },

  computed: {
    ...mapGetters(['getMediaUrl']),

    hasThumbs: function() {
      let boxThumbs = this.box?.thumbs;
      return this.useThumbs && boxThumbs !== undefined && boxThumbs[this.thumbSize] !== undefined
    },

    label: function() {
      if (this.hasLabel) {
        if (this.box.label !== null) {
          return this.box.label.name;
        } else {
          return this.box.predicted_label.name;
        }
      } else {
        return "Unknown";
      }
    },

    hasLabel: function(){
      return (this.box.label !== undefined && this.box.label !== null) || (this.box.predicted_label !== undefined && this.box.predicted_label !== null);
    },

    thumb: function() {
      let boxThumbs = this.box?.thumbs;
      if (this.useThumbs && boxThumbs !== undefined && boxThumbs[this.thumbSize] !== undefined )
        return boxThumbs[this.thumbSize]


      let fileThumbs = this.file?.thumbs;
      if (fileThumbs !== undefined && fileThumbs[this.thumbSize] !== undefined )
        return fileThumbs[this.thumbSize]


      return this.file.url;
    },

    src: function(){
      return `${this.getMediaUrl}${this.thumb}`
    },

    style: function() {
      if (this.box === undefined)
        return {}

      if (!this.hasThumbs){
        let coords = this.coordinates();

        return {
          "object-view-box": `inset(${coords.y0}% ${coords.x1}% ${coords.y1}% ${coords.x0}%)`,
          "background-image": `url(${this.src})`,
        }
      }

      return {
        "background-image": `url(${this.src})`,
      }

    },

  },

  methods: {
    coordinates: function(pad, factor) {
      if (pad === undefined)
        pad = this.pad;
      if (factor === undefined)
        factor = 100

      let {x, y, width, height} = this.box;

      let x0 = Math.max(0, Math.min(1.0, (x - pad))) * factor
      let y0 = Math.max(0, Math.min(1.0, (y - pad))) * factor
      let x1 = Math.max(0, Math.min(1.0, (1 - (x + width + pad)))) * factor
      let y1 = Math.max(0, Math.min(1.0, (1 - (y + height + pad)))) * factor

      return {x0, y0, x1, y1}
    }
  }
}


</script>


<style scoped>
.cropped-img {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;

}

.cropped-img img {
  width: 100%;
}


.cropped-img .label {
  opacity: 80%;
  position: absolute;
  inset: -12px -12px auto auto ;
  height: 24px;
  width: 24px;
  border-radius: 24px;
  border-width: 1px;
  border-style: solid;
  border-color: black !important;
  display: flex;
  justify-content: center;
  text-align: center;
}

</style>
