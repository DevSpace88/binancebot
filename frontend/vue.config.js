const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,  // ESLint beim Speichern deaktivieren
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://tradebot-api:8000',  // Bei Docker-Compose auf den Service-Namen verweisen
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        },
        logLevel: 'debug'
      }
    }
  },
  // Feature-Flags für Vue 3 explizit definieren (behebt die Warnung)
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      const featureFlags = args[0].__VUE_OPTIONS_API__ ? args[0] : args[0]['process.env'];
      featureFlags.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false;
      return args;
    });
  }
})