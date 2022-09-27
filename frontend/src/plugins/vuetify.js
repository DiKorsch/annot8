import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  icons: {
    iconfont: 'mdi', // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
  },
  theme: {
    themes: {
      light: {
        primary: '#002F5D', // brand color of Uni Jena (dark blue)
        secondary: '#EDEDED', // dark gray
        accent: '#AE9A63', // accent color of Uni Jena (gold)
      },
    },
  },
})
