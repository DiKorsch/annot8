import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';
import { gbif } from './gbif.module';
import { messages } from './messages.module';
import { pastebin } from './pastebin.module';

import DataService from '@/services/data.service';

Vue.use(Vuex);

class Crops {
  constructor(content){
    this.files = content?.files;
    this.tracks = content?.tracks;
    this.boxes = content?.boxes;
  }
}

export default new Vuex.Store({
  state: {
    project: undefined,
    projectFiles: [],
    projectCrops: new Crops(),
    loadingCrops: false,
    n_retries: 0,
    labels: [],
    tasks: [],
  },

  mutations: {
    setProjectFiles(state, files) {
      console.log("[Store] setting project files:", files)
      state.projectFiles = files || [];
    },

    setProjectCrops(state, content) {
      let crops = new Crops(content)
      console.log("[Store] setting project crops:", crops)
      state.projectCrops = crops;
      state.loadingCrops = false;
    },

    setCurrentProject(state, project) {

      if (project !== undefined){
        if (state.project?.id === project.id)
          return
        console.log("[Store] setting project:", project)
        if (state.project?.id !== project.id){
          state.projectFiles = [];
          state.projectCrops = new Crops();
          state.loadingCrops = true;

          DataService.files.get(project.id).then(
            (files) => {
              this.commit("setProjectFiles", files)
            }
          )

          DataService.crops.get(project.id, true).then(
            (crops) => {
              this.commit("setProjectCrops", crops)
            }
          )

        }

      } else
        console.log("[Store] unsetting project")

      state.project = project;
    },

    setLabels(state, labels){
      console.log("[Store] setting", labels.length, "labels")
      state.labels = labels;
    },

    setTasks(state, tasks) {
      state.tasks = tasks;
    },
    addTask(state, task) {
      state.tasks.push(task);
    },

    fileDeleted(state, file){
      if (!state.projectFiles)
        return
      console.log("[Store] removing file from store:", file)
      let i = state.projectFiles.findIndex(f => f.id == file.id);
      if (i === undefined)
        return
      state.projectFiles.splice(i, 1);
      this.dispatch("messages/info", {
            msg: `File ${file.name} deleted`})
    },

    fileUploaded(state, file){
      console.log("[Store] added file to store:", file)
      state.projectFiles.push(file)
      this.dispatch("messages/info", {
            msg: `File ${file.name} uploaded`})
    },

    bboxDeleted(state, boxId){

      const box = state.projectCrops.boxes.get(boxId);
      if (box !== undefined)
        state.projectCrops.boxes.delete(boxId)

      let deletedId = undefined;
      let i = 0;
      for (let track of state.projectCrops.tracks){

        const idx = track.indexOf(boxId)
        if (idx !== -1){
          track.splice(idx, 1)
          deletedId = i
          break
        }

        i += 1;
      }

      if (deletedId !== undefined && state.projectCrops.tracks[i].length === 0)
        state.projectCrops.tracks.splice(i, 1)
    },

    bboxLabelChanged(state, {id, label, pipeline}){

      const box = state.projectCrops.boxes.get(id);
      if (box === undefined)
        console.warn("[Store] Cannot change label of", id, "It was not found!")
      if (pipeline)
        box.predicted_label = label;
      else
        box.label = label;
    }
  },

  getters: {

    isProjectViewActive: state => {
      return state.project !== undefined;
    },

    getLabels: state => {
      return state.labels;
    },

    getCurrentProject: state => {
      return state.project;
    },

    getProjectFiles: state => {
      return state.projectFiles;
    },

    getProjectCrops: state => {
      return state.projectCrops;
    },

    getTasks: state => {
      return state.tasks;
    },

    isLoadingCrops: state => {
      return state.loadingCrops;
    },

    getAPIUrl: () => {
      return process.env.VUE_APP_API_URL;
    },

    getGBIFUrl: () => {
      return "https://api.gbif.org/v1/";
    },

    apiTimeout: () => {
      return 30 * 1000;
    },

    getMediaUrl: () => {
      return  process.env.VUE_APP_MEDIA_URL;
    },

  },

  modules: {
    auth,
    data,
    gbif,
    messages,
    pastebin,
  }
});
