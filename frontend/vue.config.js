const { defineConfig } = require('@vue/cli-service')
module.exports = {
  chainWebpack: config => {
    config.plugin('VuetifyLoaderPlugin').tap(args => [{
      match (originalTag, { kebabTag, camelTag, path, component }) {
        let packages = [
          "core", "dialogs"
        ];
        for (let package of packages){
          if (kebabTag.startsWith(`${package}-`)) {
            return [camelTag, `import ${camelTag} from '@/components/${package}/${camelTag.substring(package.length)}.vue'`]
          }
        }
      }
    }])
  },
  ...defineConfig({
    transpileDependencies: [
      'vuetify'
    ]
  })
}
