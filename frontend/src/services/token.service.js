class TokenService {

  getTokens() {
    return JSON.parse(localStorage.getItem("tokens"));
  }

  setTokens(tokens) {
    let tokens_str = JSON.stringify(tokens)
    console.log("[Token service] Setting token info in localStorage: ", tokens);
    localStorage.setItem("tokens", tokens_str);
  }

  removeTokens() {
    console.log("[Token service] Removing token info from localStorage");
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
