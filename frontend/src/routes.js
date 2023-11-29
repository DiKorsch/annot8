import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from './views/IndexView'
import Impress from './views/ImpressView'
import About from './views/AboutView'

import ListProjects from './views/project/ListView'
import CreateProject from './views/project/CreateView'
import BaseProject from './views/project/BaseView'
import ShowProject from './views/project/DetailView'
import Data from './views/project/DataView'
import Labels from './views/project/LabelsView'
import Annotations from './views/project/AnnotationsView'
import Crops from './views/project/CropsView'
import Login from './views/LoginView'
import Logout from './views/LogoutView'

//Next you need to call Vue.use(Router) to make sure that Router is added as a middleware to our Vue project.
Vue.use(VueRouter)

export default new VueRouter({
    //The default mode for Vue Router is hash mode.
    //It uses a URL hash to simulate a full URL so that the page won’t be reloaded when the URL changes.
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'index',
            component: Index,
            meta: {
                public: true
            }
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
            meta: {
              public: true
            }
        },
        {
            path: '/logout',
            name: 'logout',
            component: Logout,
        },
        {
            path: '/about',
            name: 'about',
            component: About,
            meta: {
                public: true
            }
        },
        {
            path: '/impress',
            name: 'impress',
            component: Impress,
            meta: {
                public: true
            }
        },
        {
            path: '/projects',
            name: 'projects',
            component: ListProjects,
        },
        {
            path: '/project/create',
            name: 'create_project',
            component: CreateProject,
        },
        {
          path: '/labels',
          name: 'labels',
          component: Labels
        },
        {
            path: '/project/:id',
            component: BaseProject,
            meta: {
              projectView: true,
            },

            children: [
              {
                path: 'info',
                name: 'project',
                component: ShowProject
              },
              {
                path: 'data',
                name: 'data',
                component: Data
              },
              {
                path: 'annotate',
                name: 'annotations',
                component: Annotations
              },
              {
                path: 'annotate/:fileId',
                name: 'annotate',
                component: Annotations
              },
              {
                path: 'crops',
                name: 'crops',
                component: Crops
              },
            ]
        },
    ]
})
