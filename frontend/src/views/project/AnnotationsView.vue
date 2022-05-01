<template>
  <v-container fluid>
    <v-row>
      <v-col :cols=10>
        <h1>Annotations</h1>
      </v-col>
      <v-col :cols=2 >
        <v-btn :to = "{ name: 'projects' }" block color="error">
          <v-icon>mdi-reply</v-icon> Back
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
