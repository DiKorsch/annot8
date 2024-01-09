<template>
  <div v-if="tasks.length !== 0" class="task-list white--text">
    <v-carousel
      v-model="taskId"
      height="75px"
      :show-arrows="false"
      hide-delimiter-background
      delimiter-icon="mdi-vector-point"
      >
      <v-carousel-item v-for="(task, i) in tasksSorted"
        :key="i"
      >
        <v-row
          dense
          align="center"
          justify="center"
          class="white--text"
        >
          <v-col cols=6>
            {{ task.id }}
          </v-col>
          <v-col cols=6>
            <v-progress-circular
              :rotate="-90"
              :value="progress(task) * 100"
              color="white"
              size="40"
              >
              <v-icon v-if="progress(task) >= 1.0" color="white">mdi-check</v-icon>
              <div v-else>{{Math.round(progress(task) * 100)}}%</div>
              </v-progress-circular>
          </v-col>
        </v-row>
      </v-carousel-item>
    </v-carousel>
  </div>
  <div v-else class="font-italic text-caption white--text">No active tasks in past 5 min</div>
</template>


<script>
import { mapGetters } from 'vuex'
import DataService from '@/services/data.service';

export default {
  name: "TaskList",

  data: () => ({
    timer: undefined,
    taskId: 0,
  }),

  props: {
    delay: {
      type: Number,
      default: 5000
    }
  },

  mounted() {

    if (this.timer !== undefined)
      return
    console.log("[Task List] creating new task getter")
    this.getTasks(true);
    setInterval(this.getTasks, this.delay)
  },

  unmounted() {
    if (this.timer === undefined)
      return

    console.log("[Task List] removing task getter")
    clearInterval(this.timer)
  },

  methods: {
    getTasks(force){
      if (!this.loggedIn)
        return;

      if (!force && this.allReady)
        return;

      console.log("[Task List] Checking for new tasks")
      DataService.tasks.get().then((tasks) => {
        this.$store.commit("setTasks", tasks)
      })
    },

    progress(task){
      return (task.nready||0) / task.nqueued;
    }
  },

  computed: {
    ...mapGetters('auth', [
      'loggedIn'
    ]),

    ...mapGetters({
      tasks: 'getTasks',
    }),

    tasksSorted() {
      // this will sort tasks in descending order
      return this.tasks.toSorted((a, b) => a.id === b.id ? 0 : (a.id < b.id ? 1 : -1));
    },

    allReady() {
      return this.tasks.every((task) => task.nqueued == task.nready)
    }
  }
}
</script>


<style>
.task-list .v-carousel__controls {
  height: fit-content;
}

.v-card__text:has(.task-list) {
  padding: 5px 3px 10px 3px;
}
</style>
