<template>
    <v-img
      v-if="file !== undefined"
      :src="`${getMediaUrl}${thumb}`"
      :lazy-src="`https://via.placeholder.com/150x100/?text=Image`"
      class="grey lighten-2"
      :max-height="maxHeight"
      :contain="true"
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
  computed: {
    ...mapGetters(['getMediaUrl']),

    thumb: function() {
      let thumbs = this.file?.thumbs;
      if (thumbs !== undefined && thumbs[this.thumbSize] !== undefined )
        return thumbs[this.thumbSize]

      return this.file.url;
    }
  },
}


</script>
