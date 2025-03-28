import React from 'react';
import { 
  Paper, 
  Typography, 
  Box, 
  Stack,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import MailOutlineIcon from '@mui/icons-material/MailOutline';
import SmsOutlinedIcon from '@mui/icons-material/SmsOutlined';
import { useDispatch } from 'react-redux';
import { updatePreferences } from '../store/slices/clienteSlice';

const ClientBalance = ({ clientInfo }) => {
  const dispatch = useDispatch();

  const handleChangeNotification = (event) => {
    dispatch(updatePreferences({
      clientId: clientInfo.clientId,
      data: { preferredNotification: event.target.value }
    }));
  };

  if (!clientInfo) {
    return <Paper sx={{ p: 3, mb: 3 }}>Cargando información del cliente...</Paper>;
  }

  return (
    <Paper sx={{ p: 3, mb: 3, borderRadius: 2, boxShadow: 3 }}>
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
        <AccountBalanceWalletIcon fontSize="large" color="primary" />
        <Typography variant="h5" component="h2">
          Información del Cliente
        </Typography>
      </Stack>
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="body1">
          <strong>Saldo disponible:</strong>
        </Typography>
        <Typography variant="h6" color="primary.main">
          ${clientInfo.balance?.toLocaleString()} COP
        </Typography>
      </Box>
      
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <FormControl sx={{ minWidth: 200 }} size="small">
          <InputLabel id="notification-type-label">Tipo de notificación</InputLabel>
          <Select
            labelId="notification-type-label"
            id="notification-type-select"
            value={clientInfo.preferredNotification || 'email'}
            label="Tipo de notificación"
            onChange={handleChangeNotification}
            startAdornment={
              clientInfo.preferredNotification === 'email' 
              ? <MailOutlineIcon sx={{ mr: 1 }} fontSize="small" /> 
              : <SmsOutlinedIcon sx={{ mr: 1 }} fontSize="small" />
            }
          >
            <MenuItem value="email">Email</MenuItem>
            <MenuItem value="sms">SMS</MenuItem>
          </Select>
        </FormControl>
        
        <Box>
          <Typography variant="body2" color="text.secondary">
            {clientInfo.preferredNotification === 'email' 
              ? `Email: ${clientInfo.email || 'No especificado'}`
              : `Teléfono: ${clientInfo.phone || 'No especificado'}`
            }
          </Typography>
          <Typography variant="caption" color="text.secondary">
            ID: {clientInfo.clientId}
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default ClientBalance;