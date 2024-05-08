apiVersion: v1
kind: Secret
metadata:
  name: gateway-secret
stringData:
  MONGO_CONNECTION_STRING: mongodb+srv://timkrebs9:6mXpm4sMzpp1nq2e@clipify-cluster.uzdzemn.mongodb.net/?retryWrites=true&w=majority&appName=Clipify-Cluster
  AUTH0_CLIENT_ID: jk1azzGBTY2BY58Hgl3lItz61bbvpcYr
  AUTH0_CLIENT_SECRET: jAx7UyL5lhhmISgAnN5Vs9KeygSYC5pg5f1XirnZ5W_dYuP00T_umk7RNsGbPmEo
  AUTH0_DOMAIN: dev-6ei6j58zl67xc6pm.us.auth0.com
  APP_SECRET_KEY: ALongRandomlyGeneratedString
type: Opaque