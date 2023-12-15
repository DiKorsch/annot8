import api from "./api";
import TokenService from "./token.service";
import AuthService from "./auth.service";

const setup = (store) => {
  api.interceptors.request.use(
    (config) => {
      // This adds to each request an access token
      const token = TokenService.getLocalAccessToken();
      if (token)
        config.headers["Authorization"] = `Bearer ${token}`

      return config;
    },
    (error) => {
      console.log("[API Request Interceptor] Error: ", error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (res) => {
      return res;
    },
    async (err) => {
      const originalConfig = err.config;

      // Access Token was expired
      if (originalConfig.url !== "/api-token/"
        && err.response?.status === 401
        && !originalConfig._retry) {

        console.log("[API Interceptor] Access token expired!")
        originalConfig._retry = true;
        try {
          const { access } = await AuthService.refreshAccessToken();
          console.log("[API Interceptor] New acces token: ", access)

          store.dispatch('auth/refreshToken', access);

          console.log("[API Interceptor] Retrying original request: ", originalConfig)
          return api(originalConfig);

        } catch (_error) {

          return Promise.reject(_error);
        }
      } else if (originalConfig.url === "/api-token-refresh/"){
        console.log("[API Interceptor response] Error during token refersh:", err)
      }

      return Promise.reject(err);
    }
  );
};

export default setup;
