class Message {
  constructor(content, level, timeout){
    this.content = content
    this.level = level
    this.timeout = timeout === undefined ? 3000 : timeout;
  }
}

export const messages = {
  namespaced: true,
  state: {

    consumer: undefined,
  },

  getters: {
  },

  actions: {
    info({commit}, {msg, timeout}){
      commit("newMessage", new Message(msg, "info", timeout))
    },

    alert({commit}, {msg, timeout}){
      commit("newMessage", new Message(msg, "alert", timeout))
    },

    error({commit}, {msg, timeout}){
      commit("newMessage", new Message(msg, "error", timeout))
    },


    register({commit}, consumer){
      commit("setConsumer", consumer)
    },

  },

  mutations: {
    newMessage(state, msg){
      if (state.consumer !== undefined)
        state.consumer.newMessage(msg)
    },
    setConsumer(state, consumer){
      console.log("[Messages] Setting new consumer:", consumer?.name || consumer);
      state.consumer = consumer;
    },

  }

};
