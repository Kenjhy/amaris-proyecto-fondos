// src/services/__tests__/clienteService.test.js
import { getClientInfo, updateClientPreferences } from '../clienteService';
import api from '../api';

// Mock the api module
jest.mock('../api');

describe('Cliente Service', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  describe('getClientInfo', () => {
    it('should fetch client info with default ID if none provided', async () => {
      // Setup mock response
      const mockResponse = { data: { clientId: 'C123456', balance: 500000 } };
      api.get.mockResolvedValue(mockResponse);

      // Call the function
      const result = await getClientInfo();

      // Check if API was called correctly
      expect(api.get).toHaveBeenCalledWith('/clientes/C123456');
      // Check if function returns the correct data
      expect(result).toEqual(mockResponse.data);
    });

    it('should fetch client info with provided ID', async () => {
      // Setup mock response
      const mockResponse = { data: { clientId: 'C654321', balance: 750000 } };
      api.get.mockResolvedValue(mockResponse);

      // Call the function with a specific client ID
      const result = await getClientInfo('C654321');

      // Check if API was called correctly
      expect(api.get).toHaveBeenCalledWith('/clientes/C654321');
      // Check if function returns the correct data
      expect(result).toEqual(mockResponse.data);
    });

    it('should propagate errors from the API', async () => {
      // Setup mock to throw an error
      const errorMessage = 'Network Error';
      api.get.mockRejectedValue(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getClientInfo()).rejects.toThrow(errorMessage);
      expect(api.get).toHaveBeenCalledWith('/clientes/C123456');
    });
  });

  describe('updateClientPreferences', () => {
    it('should update client preferences', async () => {
      // Setup mock data and response
      const clientId = 'C123456';
      const updateData = { 
        preferredNotification: 'email',
        email: 'test@example.com' 
      };
      const mockResponse = { 
        data: { 
          preferredNotification: 'email',
          email: 'test@example.com' 
        } 
      };
      
      api.patch.mockResolvedValue(mockResponse);

      // Call the function
      const result = await updateClientPreferences(clientId, updateData);

      // Check if API was called correctly
      expect(api.patch).toHaveBeenCalledWith(`/clientes/${clientId}`, updateData);
      // Check if function returns the correct data
      expect(result).toEqual(mockResponse.data);
    });

    it('should propagate errors from the API', async () => {
      // Setup data and mock to throw an error
      const clientId = 'C123456';
      const updateData = { preferredNotification: 'sms' };
      const errorMessage = 'Server Error';
      
      api.patch.mockRejectedValue(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(updateClientPreferences(clientId, updateData)).rejects.toThrow(errorMessage);
      expect(api.patch).toHaveBeenCalledWith(`/clientes/${clientId}`, updateData);
    });
  });
});