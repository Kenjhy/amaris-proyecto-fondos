// Usar CommonJS en lugar de ES Modules
jest.mock('axios');
// Mock axios

// Importar los servicios que queremos probar
const { getAllFunds, getFundDetails } = require('../fondoService');
const API_URL = require('../../config/api').default;
const axios = require('axios');

describe('fondoService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('getAllFunds', () => {
    test('should fetch all funds successfully', async () => {
      // Mock data
      const mockFundsData = [
        { 
          fundId: '1', 
          name: 'FPV_EL CLIENTE_RECAUDADORA', 
          category: 'FPV', 
          minimumAmount: 75000 
        },
        { 
          fundId: '2', 
          name: 'FPV_EL CLIENTE_ECOPETROL', 
          category: 'FPV', 
          minimumAmount: 125000 
        },
        { 
          fundId: '3', 
          name: 'DEUDAPRIVADA', 
          category: 'FIC', 
          minimumAmount: 50000 
        }
      ];
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockFundsData });

      // Call the function
      const result = await getAllFunds();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/fondos`);
      expect(result).toEqual(mockFundsData);
    });

    test('should return empty array when API returns empty data', async () => {
      // Setup axios mock to resolve with empty array
      axios.get.mockResolvedValueOnce({ data: [] });

      // Call the function
      const result = await getAllFunds();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/fondos`);
      expect(result).toEqual([]);
    });

    test('should propagate errors when API call fails', async () => {
      // Setup axios mock to reject with error
      const errorMessage = 'Service Unavailable';
      axios.get.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getAllFunds()).rejects.toThrow(errorMessage);
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/fondos`);
    });
  });

  describe('getFundDetails', () => {
    test('should fetch fund details successfully', async () => {
      // Mock data
      const mockFundId = '1';
      const mockFundData = { 
        fundId: mockFundId, 
        name: 'FPV_EL CLIENTE_RECAUDADORA', 
        category: 'FPV', 
        minimumAmount: 75000 
      };
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockFundData });

      // Call the function
      const result = await getFundDetails(mockFundId);

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/fondos/${mockFundId}`);
      expect(result).toEqual(mockFundData);
    });

    test('should propagate errors when fund details API call fails', async () => {
      // Mock data
      const mockFundId = '999'; // Non-existent fund
      
      // Setup axios mock to reject with error
      const errorMessage = 'Fund not found';
      axios.get.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getFundDetails(mockFundId)).rejects.toThrow(errorMessage);
      
      // Verify the axios call was made with correct parameters
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/fondos/${mockFundId}`);
    });
  });
});