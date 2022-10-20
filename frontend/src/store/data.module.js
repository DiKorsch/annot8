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

    getProjects({ commit }) {
      DataService.project.get().then(
        (projects) => {
          commit("setProjects", projects)
        })
    },

  },

  mutations : {

    setProjects(state, projects) {
      state.projects = projects;
    },
  },
}
