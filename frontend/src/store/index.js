import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';
import { messages } from './messages.module';

import DataService from '@/services/data.service';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentProject: undefined,
    projectFiles: [],
    n_retries: 0,
  },

  mutations: {
    setProjectFiles(state, files) {
      console.log("[Store] setting project files:", files)
      state.projectFiles = files || [];
    },

    setCurrentProject(state, project) {

      if (project !== undefined){
        if (state.currentProject?.id === project.id)
          return
        console.log("[Store] setting project:", project)
        if (state.currentProject?.id !== project.id)
          DataService.files.get(project.id).then(
            (files) => {
              this.commit("setProjectFiles", files)
            }
          )
      } else
        console.log("[Store] unsetting project")

      state.currentProject = project;
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
    }
  },

  getters: {

    isProjectViewActive: state => {
      return state.currentProject !== undefined;
    },

    getCurrentProject: state => {
      return state.currentProject;
    },
    getProjectFiles: state => {
      return state.projectFiles;
    },

    getAPIUrl: () => {
      return process.env.VUE_APP_API_URL;
    },

    getMediaUrl: () => {
      return  process.env.VUE_APP_MEDIA_URL;
    },

  },

  modules: {
    auth,
    data,
    messages,
  }
});
