import api from './api';

export const subscribeToFund = async (fundId) => {
  const response = await api.post('/transacciones/subscriptions', { fundId });
  return response.data;
};

export const cancelSubscription = async (fundId) => {
  const response = await api.delete(`/transacciones/subscriptions/${fundId}`);
  return response.data;
};

export const getTransactionHistory = async (limit = 10) => {
  const response = await api.get('/transacciones/history', {
    params: { limit }
  });
  return response.data;
};

export const getActiveSubscriptions = async () => {
  const response = await api.get('/transacciones/subscriptions');
  return response.data;
};