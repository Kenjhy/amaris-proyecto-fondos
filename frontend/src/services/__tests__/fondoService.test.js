// src/services/__tests__/fondoService.test.js
import { getAllFunds, getFundDetails } from '../fondoService';
import api from '../api';

// Mock the api module
jest.mock('../api');

describe('Fondo Service', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  describe('getAllFunds', () => {
    it('should fetch all funds', async () => {
      // Setup mock response with sample funds data
      const mockFunds = [
        { fundId: '1', name: 'FPV_EL CLIENTE_RECAUDADORA', category: 'FPV', minimumAmount: 75000 },
        { fundId: '2', name: 'FPV_EL CLIENTE_ECOPETROL', category: 'FPV', minimumAmount: 125000 }
      ];
      const mockResponse = { data: mockFunds };
      api.get.mockResolvedValue(mockResponse);

      // Call the function
      const result = await getAllFunds();

      // Check if API was called correctly
      expect(api.get).toHaveBeenCalledWith('/fondos');
      // Check if function returns the correct data
      expect(result).toEqual(mockFunds);
    });

    it('should propagate errors from the API', async () => {
      // Setup mock to throw an error
      const errorMessage = 'Network Error';
      api.get.mockRejectedValue(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getAllFunds()).rejects.toThrow(errorMessage);
      expect(api.get).toHaveBeenCalledWith('/fondos');
    });
  });

  describe('getFundDetails', () => {
    it('should fetch details for a specific fund', async () => {
      // Setup mock fund data and response
      const fundId = '3';
      const mockFundDetails = { 
        fundId: '3', 
        name: 'DEUDAPRIVADA', 
        category: 'FIC', 
        minimumAmount: 50000 
      };
      const mockResponse = { data: mockFundDetails };
      
      api.get.mockResolvedValue(mockResponse);

      // Call the function
      const result = await getFundDetails(fundId);

      // Check if API was called correctly
      expect(api.get).toHaveBeenCalledWith(`/fondos/${fundId}`);
      // Check if function returns the correct data
      expect(result).toEqual(mockFundDetails);
    });

    it('should propagate errors from the API', async () => {
      // Setup mock to throw an error
      const fundId = '999'; // Non-existent fund ID
      const errorMessage = 'Fund not found';
      
      api.get.mockRejectedValue(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getFundDetails(fundId)).rejects.toThrow(errorMessage);
      expect(api.get).toHaveBeenCalledWith(`/fondos/${fundId}`);
    });
  });
});