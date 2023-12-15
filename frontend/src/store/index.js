import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';
import { messages } from './messages.module';

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
      console.log("[Store] current project:", project)
      state.currentProject = project;
    },
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
