import axios from 'axios'
import store from '@/store'

const instance = axios.create({
  baseURL: store.getters.getAPIUrl,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
})

export default instance;
