<template>
  <v-container fluid>
    <app-ViewHeader title="Labels"/>
    <core-LabelList
      :parent="$route.query.parent"
    />
  </v-container>
</template>

<script>

export default {
  name: "LabelsView",
}
</script>
