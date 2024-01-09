import api from '../services/api';

export const gbif = {

  namespaced: true,
  state: {
    label: undefined,
  },

  getters: {
    getLabel: state => {
      return state.label;
    },
    getExamples(state) {
      api.get(state.label)
    },
  },

  actions : {
    setLabel({commit}, label) {
      commit("setLabel", label);
    },
    unsetLabel({commit}) {
      commit("setLabel", undefined);
    },
  },

  mutations : {

    setLabel(state, label) {
      state.label = label;
    },
  },
}
