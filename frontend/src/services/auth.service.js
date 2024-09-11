import api from "./api";
import TokenService from "./token.service";

class AuthService {
  login ({ username, password }) {
    return api.post("/api-token/", {username, password})
      .then((response) => {
        if (response.data.access)
          TokenService.setTokens(response.data);

        return response.data;
      });
  }

  logout () {
    TokenService.removeTokens();
  }

  changePassword({oldPassword, newPassword}) {
    return api.post("/user/change-password/", {
        old_password: oldPassword,
        new_password: newPassword,
      })
      .then((response) => {
        return response.data;
      });

  }

  refreshAccessToken () {

    return api.
      post("/api-token-refresh/", {
        refresh: TokenService.getLocalRefreshToken(),
      })
      .then((response) => {
        let new_token = response.data?.access
        if (new_token)
          TokenService.updateLocalAccessToken(new_token);

        return new_token;
      });
  }

}

export default new AuthService();
