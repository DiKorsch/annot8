import axios from 'axios'
import store from '@/store'

const instance = axios.create({
  baseURL: store.getters.getGBIFUrl,
  timeout: store.getters.apiTimeout,
  headers: {
    "Content-Type": "application/json",
  },
})

export default instance;
