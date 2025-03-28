jest.mock('axios');
// Usar CommonJS en lugar de ES Modules
// Mock axios

// Importar los servicios que queremos probar
const { 
  subscribeToFund, 
  cancelSubscription, 
  getTransactionHistory, 
  getActiveSubscriptions 
} = require('../transaccionService');
const API_URL = require('../../config/api').default;

const axios = require('axios');

describe('transaccionService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('subscribeToFund', () => {
    test('should subscribe to a fund successfully', async () => {
      // Mock data
      const mockFundId = '3';
      const mockResponseData = { 
        transactionId: 'tx123',
        fundId: mockFundId,
        fundName: 'DEUDAPRIVADA',
        type: 'SUBSCRIPTION',
        amount: 50000,
        status: 'COMPLETED'
      };
      
      // Setup axios mock to resolve with data
      axios.post.mockResolvedValueOnce({ data: mockResponseData });

      // Call the function
      const result = await subscribeToFund(mockFundId);

      // Assertions
      expect(axios.post).toHaveBeenCalledWith(
        `${API_URL}/transacciones/subscriptions`, 
        { fundId: mockFundId }
      );
      expect(result).toEqual(mockResponseData);
    });

    test('should propagate errors when subscription API call fails', async () => {
      // Mock data
      const mockFundId = '4';
      
      // Setup axios mock to reject with error
      const errorResponse = { 
        response: { 
          data: { 
            detail: 'No tiene saldo disponible para vincularse al fondo' 
          } 
        } 
      };
      axios.post.mockRejectedValueOnce(errorResponse);

      // Call the function and expect it to throw
      await expect(subscribeToFund(mockFundId)).rejects.toEqual(errorResponse);
      
      // Verify the axios call was made with correct parameters
      expect(axios.post).toHaveBeenCalledWith(
        `${API_URL}/transacciones/subscriptions`, 
        { fundId: mockFundId }
      );
    });
  });

  describe('cancelSubscription', () => {
    test('should cancel a subscription successfully', async () => {
      // Mock data
      const mockFundId = '1';
      const mockResponseData = { 
        transactionId: 'tx456',
        fundId: mockFundId,
        fundName: 'FPV_EL CLIENTE_RECAUDADORA',
        type: 'CANCELLATION',
        amount: 75000,
        status: 'COMPLETED'
      };
      
      // Setup axios mock to resolve with data
      axios.delete.mockResolvedValueOnce({ data: mockResponseData });

      // Call the function
      const result = await cancelSubscription(mockFundId);

      // Assertions
      expect(axios.delete).toHaveBeenCalledWith(
        `${API_URL}/transacciones/subscriptions/${mockFundId}`
      );
      expect(result).toEqual(mockResponseData);
    });

    test('should propagate errors when cancellation API call fails', async () => {
      // Mock data
      const mockFundId = '999'; // Non-existent subscription
      
      // Setup axios mock to reject with error
      const errorResponse = { 
        response: { 
          data: { 
            detail: 'No está suscrito a este fondo' 
          } 
        } 
      };
      axios.delete.mockRejectedValueOnce(errorResponse);

      // Call the function and expect it to throw
      await expect(cancelSubscription(mockFundId)).rejects.toEqual(errorResponse);
      
      // Verify the axios call was made with correct parameters
      expect(axios.delete).toHaveBeenCalledWith(
        `${API_URL}/transacciones/subscriptions/${mockFundId}`
      );
    });
  });

  describe('getTransactionHistory', () => {
    test('should fetch transaction history successfully with default limit', async () => {
      // Mock data
      const mockTransactions = [
        {
          transactionId: 'tx123',
          fundId: '1',
          fundName: 'FPV_EL CLIENTE_RECAUDADORA',
          type: 'SUBSCRIPTION',
          amount: 75000,
          transactionDate: '2025-03-27T14:30:00'
        },
        {
          transactionId: 'tx456',
          fundId: '3',
          fundName: 'DEUDAPRIVADA',
          type: 'SUBSCRIPTION',
          amount: 50000,
          transactionDate: '2025-03-26T10:15:00'
        }
      ];
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockTransactions });

      // Call the function
      const result = await getTransactionHistory();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/history`, {
        params: { limit: 10 }
      });
      expect(result).toEqual(mockTransactions);
    });

    test('should fetch transaction history with custom limit', async () => {
      // Mock data
      const customLimit = 5;
      const mockTransactions = [
        {
          transactionId: 'tx123',
          fundId: '1',
          fundName: 'FPV_EL CLIENTE_RECAUDADORA',
          type: 'SUBSCRIPTION',
          amount: 75000,
          transactionDate: '2025-03-27T14:30:00'
        }
      ];
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockTransactions });

      // Call the function with custom limit
      const result = await getTransactionHistory(customLimit);

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/history`, {
        params: { limit: customLimit }
      });
      expect(result).toEqual(mockTransactions);
    });

    test('should propagate errors when transaction history API call fails', async () => {
      // Setup axios mock to reject with error
      const errorMessage = 'Service Unavailable';
      axios.get.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getTransactionHistory()).rejects.toThrow(errorMessage);
      
      // Verify the axios call was made with correct parameters
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/history`, {
        params: { limit: 10 }
      });
    });
  });

  describe('getActiveSubscriptions', () => {
    test('should fetch active subscriptions successfully', async () => {
      // Mock data
      const mockSubscriptions = [
        {
          subscriptionId: 'sub123',
          clientId: 'C123456',
          fundId: '1',
          fundName: 'FPV_EL CLIENTE_RECAUDADORA',
          amountSubscribed: 75000,
          status: 'ACTIVE',
          subscriptionDate: '2025-03-25T09:00:00'
        },
        {
          subscriptionId: 'sub456',
          clientId: 'C123456',
          fundId: '3',
          fundName: 'DEUDAPRIVADA',
          amountSubscribed: 50000,
          status: 'ACTIVE',
          subscriptionDate: '2025-03-26T11:30:00'
        }
      ];
      
      // Setup axios mock to resolve with data
      axios.get.mockResolvedValueOnce({ data: mockSubscriptions });

      // Call the function
      const result = await getActiveSubscriptions();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/subscriptions`);
      expect(result).toEqual(mockSubscriptions);
    });

    test('should return empty array when no active subscriptions', async () => {
      // Setup axios mock to resolve with empty array
      axios.get.mockResolvedValueOnce({ data: [] });

      // Call the function
      const result = await getActiveSubscriptions();

      // Assertions
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/subscriptions`);
      expect(result).toEqual([]);
    });

    test('should propagate errors when active subscriptions API call fails', async () => {
      // Setup axios mock to reject with error
      const errorMessage = 'Service Unavailable';
      axios.get.mockRejectedValueOnce(new Error(errorMessage));

      // Call the function and expect it to throw
      await expect(getActiveSubscriptions()).rejects.toThrow(errorMessage);
      
      // Verify the axios call was made with correct parameters
      expect(axios.get).toHaveBeenCalledWith(`${API_URL}/transacciones/subscriptions`);
    });
  });
});