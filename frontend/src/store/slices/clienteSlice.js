import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getClientInfo, updateClientPreferences } from '../../services/clienteService';

export const fetchClientInfo = createAsyncThunk(
  'cliente/fetchInfo',
  async (clientId = 'C123456', { rejectWithValue }) => {
    try {
      return await getClientInfo(clientId);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const updatePreferences = createAsyncThunk(
  'cliente/updatePreferences',
  async ({ clientId = 'C123456', data }, { rejectWithValue }) => {
    try {
      return await updateClientPreferences(clientId, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const initialState = {
  clientInfo: null,
  loading: false,
  error: null
};

const clienteSlice = createSlice({
  name: 'cliente',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchClientInfo.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchClientInfo.fulfilled, (state, action) => {
        state.loading = false;
        state.clientInfo = action.payload;
      })
      .addCase(fetchClientInfo.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updatePreferences.fulfilled, (state, action) => {
        state.clientInfo = { ...state.clientInfo, ...action.payload };
      });
  }
});

export default clienteSlice.reducer;