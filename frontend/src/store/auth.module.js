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
      state.loggedIn = true;
      state.tokens = tokens;
    },
    loginFailure(state) {
      state.loggedIn = false;
      state.tokens = null;
    },
    logout(state) {
      state.loggedIn = false;
      state.tokens = null;
    },
    refreshToken(state, access) {
      state.loggedIn = true;
      state.tokens = { ...state.tokens, access: access };
    }
  }
};
