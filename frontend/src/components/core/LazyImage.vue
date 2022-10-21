<template>
    <v-img
      v-if="file !== undefined"
      :src="`${getMediaUrl}${file.url}`"
      :lazy-src="`https://via.placeholder.com/150x100/?text=Image`"
      aspect-ratio="1.333"
      class="grey lighten-2"
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
    'file': undefined,
  },
  computed: {
    ...mapGetters(['getMediaUrl']),
  },
}


</script>
