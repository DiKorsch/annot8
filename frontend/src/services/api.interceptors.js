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
      const status_code = err.response?.status;
      const has_response = err.response !== undefined

      // Access Token was expired

      const url = originalConfig.url
      console.log("[API Interceptor] error for URL:", url)
      let redirect = `/login?next=${originalConfig.url}`

      if (url !== "/api-token/"
        && url !== "/api-token-refresh/"
        && has_response
        && status_code === 401
        && !originalConfig._retry) {

        console.log("[API Interceptor] Access token expired!")
        originalConfig._retry = true;
        originalConfig._next = redirect;
        try {
          let access = await AuthService.refreshAccessToken();
          console.log("[API Interceptor] New acces token: ", access)

          store.dispatch('auth/refreshToken', access);

          console.log("[API Interceptor] Retrying original request: ", originalConfig)
          return api(originalConfig);

        } catch (_error) {

          console.log("[API Interceptor] Caught error: ", _error)
          return Promise.reject(_error);
        }

      } else if (url === "/api-token-refresh/" && has_response){
        // We have an error during token refresh!
        let data = err.response.data;
        if (status_code === 401 && data.code === "token_not_valid"){
          console.log(`[API Interceptor response] (Code ${status_code}) Refresh token was invalid! Clearing all tokens.`, err)
          store.dispatch('auth/logout');
          window.location.href = originalConfig._next || "/login/";

        } else if (status_code === 400){
          console.log(`[API Interceptor response] (Code ${status_code}) Invalid refresh request! Clearing all tokens.`, err)
          store.dispatch('auth/logout');
          window.location.href = originalConfig._next || "/login/";
        }

        // any other error except of 400 and 401
        store.dispatch("messages/error", {msg: `Error occured during token refresh: ${data.detail}`})
        console.log("[API Interceptor response] Error during token refersh:", err)
        window.location.href = originalConfig._next || "/login/";

      } else if (status_code === 401 && originalConfig._retry) {
        // despite a retry we have an unauthorized error (401)
        console.log("[API Interceptor response] Unauthorized request even after retry!", err)
        window.location.href = originalConfig._next || "/login/";
      }
      console.log("[API Interceptor response] API Interceptor was not successfull!")
      return Promise.reject(err);
    }
  );
};

export default setup;
