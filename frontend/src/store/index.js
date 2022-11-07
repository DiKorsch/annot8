import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentProject: undefined,
  },

  mutations: {
    setCurrentProject(state, id){
      state.currentProject = id;
    }
  },

  getters: {

    isProjectViewActive: state => {
      return state.currentProject !== undefined;
    },

    getCurrentProject: state => {
      return state.currentProject;
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
  }
});
