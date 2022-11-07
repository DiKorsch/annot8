import Vue from 'vue'
import App from './App.vue'
import router from './routes'
import store from './store'
import vuetify from './plugins/vuetify'
import setupInterceptors from './services/setupInterceptors';
import Vuex from 'vuex';
import DataService from '@/services/data.service';

Vue.config.productionTip = false


router.beforeEach((to, from, next) => {

  let isPublic = to.matched.some(record => record.meta.public);
  let isLoggedIn = store.state.auth.loggedIn;

  if (!isLoggedIn && !isPublic)
    next({ name: 'login' })

  let isProjectView = to.matched.some(record => record.meta.projectView);

  if (isProjectView)
      DataService.project.get(to.params.id).then(
        (project) => {
          store.commit('setCurrentProject', project);
        })
  else
    store.commit('setCurrentProject', undefined);

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
