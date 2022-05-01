import Vue from 'vue'
import App from './App.vue'
import router from './routes'
import store from './store'
import vuetify from './plugins/vuetify'
import setupInterceptors from './services/setupInterceptors';
import Vuex from 'vuex';

Vue.config.productionTip = false


router.beforeEach((to, from, next) => {

  let isPublic = to.matched.some(record => record.meta.public);
  let isLoggedIn = store.state.auth.loggedIn;

  if (!isLoggedIn && !isPublic)
    next({ name: 'login' })

  let isProjectView = to.matched.some(record => record.meta.projectView);

  let currentProject = null;
  if (isProjectView)
    currentProject = to.params.id;

  store.commit('setCurrentProject', currentProject);

  next()
})

Vue.use(Vuex);

setupInterceptors(store);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
