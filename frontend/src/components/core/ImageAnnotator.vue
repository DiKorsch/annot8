<template>
    <div align="center">
      <v-row>
        <v-col cols="auto">
          <core-ImageAnnotatorOptionBar />
        </v-col>

        <v-col>
          <core-LazyImage
            :file="file"
            thumbSize="large"
            maxHeight="675"
          >

          <core-ImageAnnotations
            :fileLabel="file.label"
            :fileId="file.id"
            />
          </core-LazyImage>
        </v-col>
      </v-row>
    </div>
</template>

<script>
export default {
  name: "ImageAnnotator",

  props: {
    file: undefined
  },

}
</script>
