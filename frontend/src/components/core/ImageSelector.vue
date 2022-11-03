<template>
  <v-container fluid>
    <v-row dense>
      <v-col cols=12>
        <v-row dense>
          <v-col
            cols=1
            v-for="image in currentImages" :key="image.id"
            @click="$emit('selected', image)"
            :class="{'active': image.id == selectedImage}"
          >
            <core-LazyImage :file="image" maxHeight="70px"/>
          </v-col>

        </v-row>
        <v-row dense>
          <v-col cols=12>
            <core-CustomPaginator v-model="page" :length="nPages"/>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "ImageSelector",

  props: {
    images: {
      type: Array,
      default: () => []
    },

    selectedImage: {
      type: Number,
      default: undefined
    }
  },

  data: () => ({
    page: 1,
  }),

  computed: {

    elementsPerPage: function() {
      return 12
    },

    nPages: function() {
      return Math.ceil(this.images.length / this.elementsPerPage)
    },

    start: function() {
      return (this.page - 1) * this.elementsPerPage;
    },

    end: function() {
      return Math.min(this.page * this.elementsPerPage, this.images.length);
    },

    currentImages: function(){
      return this.images.slice(this.start, this.end);
    },

    indexOfSelected: function(){
      const selIdx = this.selectedImage
      const idx = this.images.findIndex(
        function(image){
          return image.id == selIdx;
        });

      return idx
    },
  },

  watch: {

    images: function(){this.updatePage()},
    selectedImage: function(){this.updatePage()},

  },

  methods: {
    selectPageFor(imageId){
      this.imgIdx = imageId;
      this.updatePage()
    },
    updatePage() {
      var idx = this.indexOfSelected + 1;
      if(idx == 0)
        return

      this.page = Math.ceil(idx / this.elementsPerPage);
    }
  }
}

</script>

<style scoped>
  #selector {
    /*bottom: 0px;*/
    /*position: absolute;*/


    border: 1px dashed;
  }

  .active {
    border: 1px solid;
    border-radius: 5px;
  }
</style>
