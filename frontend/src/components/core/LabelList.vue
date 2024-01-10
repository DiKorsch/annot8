<template>
  <v-card
    elevation="2"
  >
    <v-toolbar
      color="indigo"
      dark
    >
      <v-toolbar-title v-if="labels !== undefined && labels.length !== labelList.length">
        {{labelList.length}} out of {{ labels.length }} labels
      </v-toolbar-title>
      <v-toolbar-title v-else>
        {{ labels.length }} labels
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn small @click="resetFilter"
        v-if="labels !== undefined && labels.length !== labelList.length"
      >Reset</v-btn>

      <v-spacer></v-spacer>

      <v-text-field
        v-model="searchTerm"
        placeholder="Search"
        class="center"
      />
    </v-toolbar>
    <v-container>
      <v-row
        class="px-6 py-3"
        align="center"
      >
        <span class="mr-4">Filter</span>
        <v-chip-group
          v-model="selected_ranks"
          column
          multiple
        >
          <v-chip v-for="rank in ranks"
            :key="rank"
            :value="rank"
            filter
            outlined
          >{{rank}}</v-chip>
        </v-chip-group>

      </v-row>
      <v-virtual-scroll
        :items="labelList"
        bench="5"
        height="600"
        item-height="80"
      >
        <template v-slot:default="{ item }">
          <v-list-item :key="item.id">
            <v-list-item-action>
              <v-btn
                fab
                small
                depressed
                color="primary"
              >
                {{ item.id }}
              </v-btn>
            </v-list-item-action>

            <v-list-item-content>
              <v-list-item-title>
                <v-row>
                  <v-col>
                    <div v-if="item.parent !== undefined">
                      <i>{{item.parent}}</i> > <a @click="$store.dispatch('gbif/setLabel', {label: item})">{{ item.name }}</a>
                    </div>
                    <div v-else><a @click="$store.dispatch('gbif/setLabel', {label: item})">{{ item.name }}</a></div>
                  </v-col>
                  <v-spacer/>
                  <v-col align="right">
                    <a :href="`https://gbif.org/occurrence/gallery?taxon_key=${item.id}`" target="_blank">
                      <v-icon small >
                        mdi-open-in-new
                      </v-icon>
                    </a>

                  </v-col>
                </v-row>
              </v-list-item-title>
              <v-list-item-subtitle>
              <v-chip link @click="selected_ranks=[item.rank]" class="px-auto" small> {{ item.rank }} </v-chip>
              <v-chip link :to="`?parent=${item.name}`" class="px-auto" small v-if="item.children.length">{{item.children.length }} children</v-chip>
              <v-chip class="px-auto" small v-if="item.kr_nr">K&R-Nr. {{item.kr_nr }} </v-chip>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn v-if="selectable" @click="$emit('selected', item)">Select</v-btn>
            </v-list-item-action>
          </v-list-item>

          <v-divider></v-divider>
        </template>
      </v-virtual-scroll>
    </v-container>

  </v-card>

</template>


<script>
import { mapGetters } from 'vuex'

export default {
  name: "LabelList",
  props: {
    parent: undefined,
    ranks: {
      type: Array,
      default: () => ([
        "order", "family", "genus", "species"
      ])
    },
    selectable: {
      type: Boolean,
      default: false
    },
  },

  computed: {

    ...mapGetters({labels: "getLabels"}),

    labelList: function(){
      if (this.labels === undefined)
        return [];
      let result = this.labels;

      if (this.parent !== undefined)
        result = result.filter(
          (label) => label.parent == this.parent
        );
      if (this.selected_ranks.length > 0)
        result = result.filter(
          (label) => this.selected_ranks.includes(label.rank)
        );
      if (this.searchTerm !== undefined)
        result = result.filter(
          (label) => label.contains(this.searchTerm.toLowerCase())
        );

      return result;
    }
  },

  data: () => ({

    selected_ranks: [],
    searchTerm: undefined,
  }),

  methods: {
    resetFilter(){
      this.selected_ranks = [];
      this.searchTerm = undefined;
      if (this.$route.query?.parent !== undefined)
        this.$router.replace({
          name: 'labels',
          params: {id: this.$route.params.id},
          query: {}
        })
    }
  }
}
</script>
