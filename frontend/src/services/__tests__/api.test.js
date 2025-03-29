// src/services/__tests__/api.test.js
import API_URL from '../../config/api';

// Mock axios
jest.mock('axios');
import axios from 'axios';

// Importamos la función createApi en lugar de la instancia por defecto
import { createApi } from '../api';

describe('API Service', () => {
  it('should create API instance with correct configuration', () => {
    // Llamamos a la función directamente en el test
    createApi();
    
    // Ahora podemos verificar que axios.create fue llamado con los parámetros correctos
    expect(axios.create).toHaveBeenCalledWith({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  });
});