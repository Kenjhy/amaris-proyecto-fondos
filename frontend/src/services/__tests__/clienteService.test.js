// Usar CommonJS en lugar de ES Modules
jest.mock('axios');

// Mock axios

// Importar los servicios que queremos probar
const { getClientInfo, updateClientPreferences } = require('../clienteService');
const API_URL = require('../../config/api').default;

const axios = require('axios');

describe('clienteService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('getClientInfo', () => {
    test('should fetch client info successfully', async () => {
      // Mock data
      const mockClientData = { 
        clientId: 'C123456', 
        balance: 500000, 
        preferredNotification: 'email',
        email: 'test@example.com' 
      };
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockClientData });

      // Call the function
      const result = await getClientInfo();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/clientes/C123456`);
      expect(result).toEqual(mockClientData);
    });

    test('should fetch client info with provided client ID', async () => {
      // Mock data
      const mockClientId = 'C654321';
      const mockClientData = { 
        clientId: mockClientId, 
        balance: 750000, 
        preferredNotification: 'sms',
        phone: '+1234567890' 
      };
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockClientData });

      // Call the function with a specific client ID
      const result = await getClientInfo(mockClientId);

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/clientes/${mockClientId}`);
      expect(result).toEqual(mockClientData);
    });

    test('should propagate errors when API call fails', async () => {
      // Setup axios mock to reject with error
      const errorMessage = 'Network Error';
      axios.get.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getClientInfo()).rejects.toThrow(errorMessage);
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/clientes/C123456`);
    });
  });

  describe('updateClientPreferences', () => {
    test('should update client preferences successfully', async () => {
      // Mock data
      const mockClientId = 'C123456';
      const mockUpdateData = { 
        preferredNotification: 'sms',
        phone: '+1234567890' 
      };
      const mockResponse = { 
        preferredNotification: 'sms',
        phone: '+1234567890' 
      };
      
      // Setup axios mock to resolve with data
      axios.patch.mockResolvedValueOnce({ data: mockResponse });

      // Call the function
      const result = await updateClientPreferences(mockClientId, mockUpdateData);

      // Assertions
      expect(axios.patch).toHaveBeenCalledWith(
        `${API_URL}/clientes/${mockClientId}`, 
        mockUpdateData
      );
      expect(result).toEqual(mockResponse);
    });

    test('should propagate errors when update API call fails', async () => {
      // Mock data
      const mockClientId = 'C123456';
      const mockUpdateData = { preferredNotification: 'email' };
      
      // Setup axios mock to reject with error
      const errorMessage = 'Bad Request';
      axios.patch.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(updateClientPreferences(mockClientId, mockUpdateData))
        .rejects.toThrow(errorMessage);
      
      // Verify the axios call was made with correct parameters
      expect(axios.patch).toHaveBeenCalledWith(
        `${API_URL}/clientes/${mockClientId}`, 
        mockUpdateData
      );
    });
  });
});