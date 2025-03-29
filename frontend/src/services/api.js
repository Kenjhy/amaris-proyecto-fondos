// src/services/api.js
import axios from 'axios';
import API_URL from '../config/api';

// Exportamos la función createApi para poder probarla directamente
export const createApi = () => {
  return axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json'
    }
  });
};

// Exportamos la instancia por defecto
const api = createApi();
export default api;