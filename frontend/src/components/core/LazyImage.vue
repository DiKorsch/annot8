<template>
    <v-img
      v-if="file !== undefined"
      ref="vImg"
      :src="`${getMediaUrl}${thumb}`"
      :lazy-src="`${getMediaUrl}${lazySrc}`"
      class="grey lighten-2"
      :max-height="maxHeight"
      :max-width="maxWidth"
      :contain="true"
      :aspect-ratio="ratio"
      @load="loaded"
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

      <slot></slot>
    </v-img>
</template>


<script>
import { mapGetters } from 'vuex';
export default {
  name: "LazyImage",

  props: {
    file: undefined,
    thumbSize: {
      type:  String,
      default: 'small',
    },
    maxHeight: undefined,
  },

  data: () => ({
    ratio: 1.0,
  }),
  computed: {
    ...mapGetters(['getMediaUrl']),

    thumb: function() {
      let thumbs = this.file?.thumbs;
      if (thumbs !== undefined && thumbs[this.thumbSize] !== undefined )
        return thumbs[this.thumbSize]

      return this.file.url;
    },

    lazySrc: function(){

      let thumbs = this.file?.thumbs;
      if (thumbs !== undefined && thumbs["small"] !== undefined )
        return thumbs["small"]

      return "https://via.placeholder.com/150x100/?text=Image";
    },

    maxWidth: function() {
      return this.ratio * this.maxHeight;
    }
  },

  methods: {
    loaded: function() {
      let img = this.$refs.vImg.image;
      this.ratio = img.width / img.height;
    }
  }
}


</script>
