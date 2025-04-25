const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://tradebot-api:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        },
        logLevel: 'debug'
      }
    }
  },
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      const existing = args[0]['process.env'] || args[0];
      existing.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = 'false';
      existing.__VUE_PROD_DEVTOOLS_GLOBAL_HOOK__ = 'false';
      existing.__VUE_OPTIONS_API__ = 'true';
      return args;
    });
  }
})