import { configureStore } from '@reduxjs/toolkit';
import clienteReducer from './slices/clienteSlice';
import fondoReducer from './slices/fondoSlice';
import transaccionReducer from './slices/transaccionSlice';

export const store = configureStore({
  reducer: {
    cliente: clienteReducer,
    fondo: fondoReducer,
    transaccion: transaccionReducer
  }
});