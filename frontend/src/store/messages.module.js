class Message {
  constructor(content, level, timeout = 5000){
    console.log("[Messages] New message created:", level, content)
    this.content = content
    this.level = level
    this.timeout = timeout
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
    info({commit}, content){
      commit("newMessage", new Message(content, "info"))
    },

    alert({commit}, content){
      commit("newMessage", new Message(content, "alert"))
    },

    error({commit}, content){
      commit("newMessage", new Message(content, "error"))
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
