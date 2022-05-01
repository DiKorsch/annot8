import api from "./api";
import TokenService from "./token.service";

class AuthService {
  login ({ username, password }) {
    return api
      .post("/api-token/", {username, password})
      .then((response) => {
        if (response.data.access)
          TokenService.setTokens(response.data);

        return response.data;
      });
  }

  logout () {
    TokenService.removeTokens();
  }

  refreshAccessToken () {

    return api.
      post("/api-token-refresh/", {
        refresh: TokenService.getLocalRefreshToken(),
      })
      .then((response) => {
        if (response.data.access)
          TokenService.updateLocalAccessToken(response.data.access);

        return response.data;
      });
  }

}

export default new AuthService();
