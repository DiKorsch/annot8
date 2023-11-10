<template>
  <div>
  <v-row>
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
  },

  data: () => ({
    pad: 0.00,
    // imgSize: undefined,
    thumbSize: "medium",
    thumbSizes: [
      {key: "small", text: "Low"},
      {key: "medium", text: "Medium"},
      {key: "large", text: "High"},
      {key: undefined, text: "Original"},
    ],
  }),
  computed: {
    ...mapGetters(['getMediaUrl']),

    thumb: function() {

      let thumbs = this.file?.thumbs;
      if (thumbs !== undefined && thumbs[this.thumbSize] !== undefined )
        return thumbs[this.thumbSize]

      return this.file.url;
    },

    src: function(){
      return `${this.getMediaUrl}${this.thumb}`
    },

    style: function() {
      if (this.box === undefined)
        return {}

      let coords = this.coordinates();

      return {
        "object-view-box": `inset(${coords.y0}% ${coords.x1}% ${coords.y1}% ${coords.x0}%)`,
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

</style>
