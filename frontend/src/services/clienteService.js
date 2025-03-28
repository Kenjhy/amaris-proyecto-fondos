import api from './api';

export const getClientInfo = async (clientId = 'C123456') => {
  const response = await api.get(`/clientes/${clientId}`);
  return response.data;
};

export const updateClientPreferences = async (clientId, data) => {
  const response = await api.patch(`/clientes/${clientId}`, data);
  return response.data;
};