
export const pastebin = {

  namespaced: true,
  state: {
    storedObject: undefined,
  },

  getters: {
    get: state => {
      return state.storedObject;
    },
    isSet: state => {
      return state.storedObject !== undefined;
    }
  },

  actions: {
    store({commit}, obj){
      commit("set", obj)
    },
    reset({commit}){
      commit("set", undefined)
    }
  },
  mutations: {
    set(state, obj){
      console.log("[PasteBin] storing new object:", obj);
      state.storedObject = obj;
    }
  }
}
