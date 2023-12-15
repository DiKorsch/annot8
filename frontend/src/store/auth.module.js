import AuthService from '../services/auth.service';
import TokenService from '../services/token.service';

const tokens = TokenService.getTokens();
const initialState = tokens
  ? { loggedIn: true , tokens }
  : { loggedIn: false , tokens: null };

export const auth = {
  namespaced: true,
  state: initialState,

  getters: {
    username: state => {
      return state.tokens?.username;
    },

    loggedIn: state => {
      return state.tokens !== null;
    }
  },

  actions: {
    login({ commit }, user) {
      return AuthService.login(user).then(
        tokens => {
          commit('loginSuccess', tokens);
          return Promise.resolve(tokens);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    refreshToken({ commit }, access) {
      commit('refreshToken', access);
    }
  },
  mutations: {
    loginSuccess(state, tokens) {
      console.log("[Store Auth] login success:", tokens)
      state.loggedIn = true;
      state.tokens = tokens;
      this.dispatch("messages/info", `Logged in as ${tokens.username}`)
    },
    loginFailure(state) {
      console.log("[Store Auth] login failure!")
      state.loggedIn = false;
      state.tokens = null;
      this.dispatch("messages/alert", "Logged failed!")
    },
    logout(state) {
      console.log("[Store Auth] logged out!")
      state.loggedIn = false;
      state.tokens = null;
      this.dispatch("messages/info", "Logged out")
    },
    refreshToken(state, access) {
      console.log("[Store Auth] refreshing access token:", access)
      state.loggedIn = true;
      state.tokens = { ...state.tokens, access: access };
    }
  }
};
