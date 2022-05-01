import api from "./api";
import TokenService from "./token.service";
import AuthService from "./auth.service";

const setup = (store) => {
  api.interceptors.request.use(
    (config) => {
      const token = TokenService.getLocalAccessToken();
      if (token)
        config.headers["Authorization"] = `Bearer ${token}`

      return config;
    },
    (error) => {
      console.log(error);
      return Promise.reject(error);
    }
  );

  api.interceptors.response.use(
    (res) => {
      return res;
    },
    async (err) => {
      const originalConfig = err.config;

      if (originalConfig.url !== "/api-token/" && err.response) {
        // Access Token was expired
        if (err.response.status === 401 && !originalConfig._retry) {

          console.log("Access token expired!")
          originalConfig._retry = true;
          try {
            const { access } = await AuthService.refreshAccessToken();
            console.log("New acces token: ", access)

            store.dispatch('auth/refreshToken', access);

            console.log("Retrying original request")
            return api(originalConfig);

          } catch (_error) {

            return Promise.reject(_error);
          }
        }
      }

      return Promise.reject(err);
    }
  );
};

export default setup;
