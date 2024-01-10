<template>

    <v-bottom-sheet
      v-model="hasLabel"
      inset
      >
      <v-card class="mx-auto" v-if="label !== undefined">
        <v-card-title>
          Examples from GBIF for "{{label.name}}"
          <a :href="gbif_link(label)" target="_new">
            <v-icon right>mdi-open-in-new</v-icon>
          </a>
          <v-spacer/>
          <v-btn @click="loadResults">reload</v-btn>

        </v-card-title>
        <v-card-text>
          <v-row v-if="examples.length !== 0">
            <v-col
              v-for="(ex, i) in examples"
              :key="i"
              cols=3
              >
              <a target="_new" :href="ex.identifier">
                <v-img
                  :src="ex.identifier"
                  aspect-ratio="1.778"
                  max-height="240">
                </v-img>
              </a>
              <v-list>
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>Source:</v-list-item-title>
                    <span class="text-truncate" :title="ex.source">{{ex.source}}</span>
                  </v-list-item-content>
                </v-list-item>

                <v-list-item v-if="ex.creator">

                  <v-list-item-content>
                    <v-list-item-title>Created by</v-list-item-title>
                    {{ex.creator}}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="ex.license">
                  <v-list-item-content>
                    <v-list-item-title>License:</v-list-item-title>
                     {{ex.license}}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-alert v-else
            border="top"
            type="warning"
            colored-border
            elevation="2"
          >
            There were no example images
          </v-alert>
        </v-card-text>
        <div v-if="reference !== undefined">
          <v-card-title>Your reference:</v-card-title>
          <v-card-text>
            <v-img
              contain
              :src="reference"
              aspect-ratio="1.778"
              max-height="240">
            </v-img>
          </v-card-text>
        </div>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            text
            color="red"
            @click="hasLabel = false"
          >
            close
          </v-btn>

        </v-card-actions>
      </v-card>

      <v-alert v-else
          border="top"
          type="warning"
          colored-border
          elevation="2"
        >
          There were no example images
        </v-alert>
    </v-bottom-sheet>
</template>


<script>
import { mapGetters } from 'vuex'
import gbif from "@/services/gbif";


export default {
  name: "GBIFExamples",

  data: () => ({
    gbifResults: undefined,
    maxExamples: 4
  }),

  computed: {

    ...mapGetters("gbif",{
      label: 'getLabel',
      reference: 'getReference',
    }),

    hasLabel: {
      get() { return this.label?.id !== undefined },
      set() { this.$store.dispatch("gbif/unsetLabel")}
    },

    examples() {
      let res = [];
      if (this.gbifResults === undefined)
        return res

      var chosen = [];
      var i = Math.min(this.gbifResults.length, this.maxExamples);
      for (; i > 0; i--) {

        var idx = undefined;
        while (idx === undefined || chosen.includes(idx))
          idx = Math.floor(this.gbifResults.length * Math.random());

        chosen.push(idx);
        res.push(this.gbifResults[idx]);
      }
      return res
    }


  },

  methods: {

    gbif_link(label){
      return `https://www.gbif.org/occurrence/gallery?media_type=StillImage&life_stage=Imago&taxon_key=${label.id}`
    },

    loadResults() {

      if(this.label !== undefined)

        gbif.get(`species/${this.label.id}/media?limit=10&life_stage=Imago&media_type=StillImage`)
          .then((response) => {
            this.gbifResults = response?.data?.results
          })
      else
        this.gbifResults = undefined
    },

  },

  watch: {
    label(){
      this.loadResults()
    }
  }

}
</script>
