// src/services/__tests__/transaccionService.test.js
import { 
    subscribeToFund, 
    cancelSubscription, 
    getTransactionHistory, 
    getActiveSubscriptions 
  } from '../transaccionService';
  import api from '../api';
  
  // Mock the api module
  jest.mock('../api');
  
  describe('Transaccion Service', () => {
    beforeEach(() => {
      // Clear all mocks before each test
      jest.clearAllMocks();
    });
  
    describe('subscribeToFund', () => {
      it('should create a fund subscription', async () => {
        // Setup mock data and response
        const fundId = '1';
        const mockResponse = { 
          data: { 
            transactionId: 'T12345',
            fundId: '1',
            type: 'SUBSCRIPTION',
            amount: 75000,
            status: 'COMPLETED',
            fundName: 'FPV_EL CLIENTE_RECAUDADORA'
          } 
        };
        
        api.post.mockResolvedValue(mockResponse);
  
        // Call the function
        const result = await subscribeToFund(fundId);
  
        // Check if API was called correctly
        expect(api.post).toHaveBeenCalledWith('/transacciones/subscriptions', { fundId });
        // Check if function returns the correct data
        expect(result).toEqual(mockResponse.data);
      });
  
      it('should propagate errors from the API', async () => {
        // Setup data and mock to throw an error
        const fundId = '1';
        const errorMessage = 'Insufficient funds';
        
        api.post.mockRejectedValue(new Error(errorMessage));
  
        // Call the function and expect it to throw
        await expect(subscribeToFund(fundId)).rejects.toThrow(errorMessage);
        expect(api.post).toHaveBeenCalledWith('/transacciones/subscriptions', { fundId });
      });
    });
  
    describe('cancelSubscription', () => {
      it('should cancel a fund subscription', async () => {
        // Setup mock data and response
        const fundId = '1';
        const mockResponse = { 
          data: { 
            transactionId: 'T67890',
            fundId: '1',
            type: 'CANCELLATION',
            amount: 75000,
            status: 'COMPLETED',
            fundName: 'FPV_EL CLIENTE_RECAUDADORA'
          } 
        };
        
        api.delete.mockResolvedValue(mockResponse);
  
        // Call the function
        const result = await cancelSubscription(fundId);
  
        // Check if API was called correctly
        expect(api.delete).toHaveBeenCalledWith(`/transacciones/subscriptions/${fundId}`);
        // Check if function returns the correct data
        expect(result).toEqual(mockResponse.data);
      });
  
      it('should propagate errors from the API', async () => {
        // Setup data and mock to throw an error
        const fundId = '999'; // Non-existent subscription
        const errorMessage = 'Subscription not found';
        
        api.delete.mockRejectedValue(new Error(errorMessage));
  
        // Call the function and expect it to throw
        await expect(cancelSubscription(fundId)).rejects.toThrow(errorMessage);
        expect(api.delete).toHaveBeenCalledWith(`/transacciones/subscriptions/${fundId}`);
      });
    });
  
    describe('getTransactionHistory', () => {
      it('should fetch transaction history with default limit', async () => {
        // Setup mock response
        const mockTransactions = [
          { transactionId: 'T1', type: 'SUBSCRIPTION', amount: 75000 },
          { transactionId: 'T2', type: 'CANCELLATION', amount: 50000 }
        ];
        const mockResponse = { data: mockTransactions };
        
        api.get.mockResolvedValue(mockResponse);
  
        // Call the function with default limit
        const result = await getTransactionHistory();
  
        // Check if API was called correctly with default params
        expect(api.get).toHaveBeenCalledWith('/transacciones/history', {
          params: { limit: 10 }
        });
        // Check if function returns the correct data
        expect(result).toEqual(mockTransactions);
      });
  
      it('should fetch transaction history with custom limit', async () => {
        // Setup mock response
        const mockTransactions = [
          { transactionId: 'T1', type: 'SUBSCRIPTION', amount: 75000 }
        ];
        const mockResponse = { data: mockTransactions };
        
        api.get.mockResolvedValue(mockResponse);
  
        // Call the function with custom limit
        const result = await getTransactionHistory(1);
  
        // Check if API was called correctly with custom params
        expect(api.get).toHaveBeenCalledWith('/transacciones/history', {
          params: { limit: 1 }
        });
        // Check if function returns the correct data
        expect(result).toEqual(mockTransactions);
      });
  
      it('should propagate errors from the API', async () => {
        // Setup mock to throw an error
        const errorMessage = 'Server Error';
        
        api.get.mockRejectedValue(new Error(errorMessage));
  
        // Call the function and expect it to throw
        await expect(getTransactionHistory()).rejects.toThrow(errorMessage);
        expect(api.get).toHaveBeenCalledWith('/transacciones/history', {
          params: { limit: 10 }
        });
      });
    });
  
    describe('getActiveSubscriptions', () => {
      it('should fetch active subscriptions', async () => {
        // Setup mock response
        const mockSubscriptions = [
          { 
            subscriptionId: 'S1', 
            fundId: '1', 
            status: 'ACTIVE', 
            amountSubscribed: 75000,
            fundName: 'FPV_EL CLIENTE_RECAUDADORA'
          }
        ];
        const mockResponse = { data: mockSubscriptions };
        
        api.get.mockResolvedValue(mockResponse);
  
        // Call the function
        const result = await getActiveSubscriptions();
  
        // Check if API was called correctly
        expect(api.get).toHaveBeenCalledWith('/transacciones/subscriptions');
        // Check if function returns the correct data
        expect(result).toEqual(mockSubscriptions);
      });
  
      it('should propagate errors from the API', async () => {
        // Setup mock to throw an error
        const errorMessage = 'Server Error';
        
        api.get.mockRejectedValue(new Error(errorMessage));
  
        // Call the function and expect it to throw
        await expect(getActiveSubscriptions()).rejects.toThrow(errorMessage);
        expect(api.get).toHaveBeenCalledWith('/transacciones/subscriptions');
      });
    });
  });