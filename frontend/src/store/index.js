import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    apiURL: "http://127.0.0.1:5000/api/v1",
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
    }

  },

  modules: {
    auth,
    data,
  }
});
