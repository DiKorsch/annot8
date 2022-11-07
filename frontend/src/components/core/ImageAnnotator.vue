<template>

    <div align="center">

        <core-LazyImage
          :file="file"
          thumbSize="large"
          maxHeight="675"
        >

        <core-ImageAnnotations
          :annotations="file.annotations"
        />
      </core-LazyImage>
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
