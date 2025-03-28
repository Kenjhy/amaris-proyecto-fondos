import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getAllFunds, getFundDetails } from '../../services/fondoService';

export const fetchAllFunds = createAsyncThunk(
  'fondo/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      return await getAllFunds();
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchFundDetails = createAsyncThunk(
  'fondo/fetchDetails',
  async (fundId, { rejectWithValue }) => {
    try {
      return await getFundDetails(fundId);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const initialState = {
  fundsList: [],
  currentFund: null,
  loading: false,
  error: null
};

const fondoSlice = createSlice({
  name: 'fondo',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fondos todos
      .addCase(fetchAllFunds.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAllFunds.fulfilled, (state, action) => {
        state.loading = false;
        state.fundsList = action.payload;
      })
      .addCase(fetchAllFunds.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fondo específico
      .addCase(fetchFundDetails.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFundDetails.fulfilled, (state, action) => {
        state.loading = false;
        state.currentFund = action.payload;
      })
      .addCase(fetchFundDetails.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export default fondoSlice.reducer;