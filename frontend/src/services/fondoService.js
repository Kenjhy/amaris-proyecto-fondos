import api from './api';

export const getAllFunds = async () => {
  const response = await api.get('/fondos');
  return response.data;
};

export const getFundDetails = async (fundId) => {
  const response = await api.get(`/fondos/${fundId}`);
  return response.data;
};