export const gbif = {

  namespaced: true,
  state: {
    label: undefined,
    reference: undefined,
  },

  getters: {
    getLabel: state => {
      return state.label;
    },

    getReference: state => {
      return state.reference;
    }
  },

  actions : {
    setLabel({commit}, {label, reference}) {
      commit("setLabel", label);
      commit("setReference", reference);
    },

    unsetLabel({commit}) {
      commit("setLabel", undefined);
      commit("setReference", undefined);
    },
  },

  mutations : {

    setLabel(state, label) {
      state.label = label;
    },

    setReference(state, reference) {
      state.reference = reference;
    },
  },
}
