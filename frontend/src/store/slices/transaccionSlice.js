import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { 
  subscribeToFund, 
  cancelSubscription, 
  getTransactionHistory, 
  getActiveSubscriptions 
} from '../../services/transaccionService';

export const fetchTransactionHistory = createAsyncThunk(
  'transaccion/fetchHistory',
  async (limit = 10, { rejectWithValue }) => {
    try {
      return await getTransactionHistory(limit);
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || "Error desconocido");
    }
  }
);

export const fetchActiveSubscriptions = createAsyncThunk(
  'transaccion/fetchActiveSubscriptions',
  async (_, { rejectWithValue }) => {
    try {
      return await getActiveSubscriptions();
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || "Error desconocido");
    }
  }
);

export const subscribeToFundAction = createAsyncThunk(
  'transaccion/subscribeToFund',
  async (fundId, { rejectWithValue }) => {
    try {
      return await subscribeToFund(fundId);
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || "Error al suscribirse");
    }
  }
);

export const cancelFundSubscription = createAsyncThunk(
  'transaccion/cancelSubscription',
  async (fundId, { rejectWithValue }) => {
    try {
      return await cancelSubscription(fundId);
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || error.message || "Error al cancelar");
    }
  }
);

const initialState = {
  transactions: [],
  activeSubscriptions: [],
  loading: false,
  error: null,
  lastOperation: null
};

const transaccionSlice = createSlice({
  name: 'transaccion',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearLastOperation: (state) => {
      state.lastOperation = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Historial de transacciones
      .addCase(fetchTransactionHistory.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTransactionHistory.fulfilled, (state, action) => {
        state.loading = false;
        state.transactions = action.payload || [];
      })
      .addCase(fetchTransactionHistory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.transactions = [];
      })
      // Suscripciones activas
      .addCase(fetchActiveSubscriptions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchActiveSubscriptions.fulfilled, (state, action) => {
        state.loading = false;
        state.activeSubscriptions = action.payload || [];
      })
      .addCase(fetchActiveSubscriptions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.activeSubscriptions = [];
      })
      // Suscribir a fondo
      .addCase(subscribeToFundAction.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(subscribeToFundAction.fulfilled, (state, action) => {
        state.loading = false;
        state.lastOperation = {
          type: 'SUBSCRIPTION',
          data: action.payload,
          success: true
        };
      })
      .addCase(subscribeToFundAction.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.lastOperation = {
          type: 'SUBSCRIPTION',
          success: false,
          error: action.payload
        };
      })
      // Cancelar suscripción
      .addCase(cancelFundSubscription.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(cancelFundSubscription.fulfilled, (state, action) => {
        state.loading = false;
        state.lastOperation = {
          type: 'CANCELLATION',
          data: action.payload,
          success: true
        };
      })
      .addCase(cancelFundSubscription.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.lastOperation = {
          type: 'CANCELLATION',
          success: false,
          error: action.payload
        };
      });
  }
});

export const { clearError, clearLastOperation } = transaccionSlice.actions;
export default transaccionSlice.reducer;