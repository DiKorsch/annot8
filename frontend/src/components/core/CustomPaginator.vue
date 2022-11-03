<template>
  <v-row justify="center" v-if="length > 1">
    <v-col cols="8">
        <v-pagination
          v-model="localValue"
          :length="length"
        />
    </v-col>
  </v-row>
</template>


<script>
export default {
  name: "CustomPaginator",
  model: {prop: "value", event: "input"},

  props: {
    value: {type: Number, default: undefined},
    length: {type: Number, default: undefined},
  },

  computed: {
    localValue: {
      get: function(){ return this.value },
      set: function(value){ this.$emit('input', value) },
    }
  },

}
</script>
