import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    apiURL: "http://127.0.0.1:8000/annot8/api/v1",
    mediaURL: "http://127.0.0.1:8000",
    currentProject: null,
  },

  mutations: {
    setCurrentProject(state, id){
      state.currentProject = id;
    }
  },

  getters: {

    isProjectViewActive: state => {
      return state.currentProject !== null;
    },

    getCurrentProject: state => {
      return state.currentProject;
    },

    getAPIUrl: state => {
      return state.apiURL;
    },

    getMediaUrl: state => {
      return state.mediaURL;
    },

  },

  modules: {
    auth,
    data,
  }
});
