class TokenService {

  getTokens() {
    return JSON.parse(localStorage.getItem("tokens"));
  }

  setTokens(tokens) {
    let tokens_str = JSON.stringify(tokens)
    console.log("Setting token info: ", tokens_str);
    localStorage.setItem("tokens", tokens_str);
  }

  removeTokens() {
    localStorage.removeItem("tokens");
  }

  getLocalRefreshToken() {
    const tokens = this.getTokens();
    return tokens?.refresh;
  }

  getLocalAccessToken() {
    const tokens = this.getTokens();
    return tokens?.access;
  }

  updateLocalAccessToken(token) {
    let tokens = this.getTokens();
    tokens.access = token;
    this.setTokens(tokens);
  }

}

export default new TokenService();
