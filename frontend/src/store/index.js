import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import { data } from './data.module';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentProject: undefined,
    projectFiles: [],
    conn: undefined,
    n_retries: 0,
  },

  mutations: {
    setProjectFiles(state, files) {
      console.log("[Store] setting project files:", files)
      state.projectFiles = files || [];
    },

    setCurrentProject(state, project) {
      console.log("[Store] current project:", project)
      state.currentProject = project;
      if (project === undefined){
        if (state.conn !== undefined)
          state.conn.close()
        return
      }

      if (state.conn === undefined) {
        let URL = this.getters.getWebSocketUrl;
        let connect = function(){
          console.log("[Store] creating new WS connection for project", project.id);
          state.n_retries++;

          new_WS_Connection(URL, project.id,
            // callbacks
            {
              onopen: function(event){
                console.log("[Project WS] Connected:", event)
                state.conn = event.target;
                state.n_retries = 0;
                event.target.send(JSON.stringify({"message": "hello world!"}))
              },

              onmessage: function(e){

                let data = JSON.parse(e.data);
                console.log("[Project WS] Data:", data)
              },
              onclose: function(){
                state.conn = undefined;
                console.log("[Project WS] Closed connection for project", project.id);

                if (state.currentProject === undefined) {
                  console.log("[Project WS] Project unset, so no reconnection will be attempted");

                } else if (state.n_retries >= 5 ) {
                  let sec = 60;
                  console.log(`[Project WS] Reconnection failed after ${state.n_retries} tries. Next attemt in ${sec}sec`);
                  state.n_retries = 0
                  setTimeout(connect, sec*1000)

                } else{
                  let sec = 3;
                  console.log(`[Project WS] (${state.n_retries}) Reconnecting after ${sec}sec`);
                  setTimeout(connect, sec*1000)
                }
              },

            }
          )

        }

        connect();
      }
    },
  },

  getters: {

    isProjectViewActive: state => {
      return state.currentProject !== undefined;
    },

    getCurrentProject: state => {
      return state.currentProject;
    },
    getProjectFiles: state => {
      return state.projectFiles;
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
