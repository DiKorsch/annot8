import DataService from '../services/data.service';

export const data = {

  namespaced: true,
  state: {
    models: [],
    labelProviders: [],
    projects: [],
  },

  getters: {
    getProjects: state => {
      return state.projects;
    }
  },

  actions : {
    getModels({ commit }) {
      DataService.getModels().then(
        (models) => {
          commit("setModels", models)
        })
    },

    getLabelProviders({ commit }) {
      DataService.getLabelProviders().then(
        (labelProviders) => {
          commit("setLabelProviders", labelProviders)
        })
    },

    getProjects({ commit }) {
      DataService.getProjects().then(
        (projects) => {
          commit("setProjects", projects)
        })
    },

  },

  mutations : {

    setModels(state, models) {
      state.models = models;
    },

    setLabelProviders(state, labelProviders) {
      state.labelProviders = labelProviders;
    },

    setProjects(state, projects) {
      state.projects = projects;
    },
  },
}
