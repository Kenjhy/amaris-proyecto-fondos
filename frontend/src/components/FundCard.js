import React from 'react';
import { 
  Card, 
  CardContent, 
  CardActions, 
  Typography, 
  Button,
  Chip,
  Box,
  Tooltip
} from '@mui/material';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import CategoryIcon from '@mui/icons-material/Category';

const FundCard = ({ fund, onSubscribe, onCancel, isSubscribed, clientBalance }) => {
  // Verificar si el cliente tiene saldo suficiente para suscribirse
  const canSubscribe = clientBalance >= fund.minimumAmount;
  
  return (
    <Card sx={{ width: '100%', mb: 2, borderRadius: 2, boxShadow: 3 }}>
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom>
          {fund.name}
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <CategoryIcon fontSize="small" sx={{ color: 'text.secondary', mr: 1 }} />
          <Chip 
            label={fund.category} 
            size="small" 
            color={fund.category === 'FPV' ? 'primary' : 'secondary'} 
            variant="outlined"
          />
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <AccountBalanceWalletIcon fontSize="small" sx={{ color: 'text.secondary', mr: 1 }} />
          <Typography variant="body2" color="text.secondary">
            Monto mínimo: ${fund.minimumAmount.toLocaleString()} COP
          </Typography>
        </Box>
      </CardContent>
      
      <CardActions sx={{ justifyContent: 'flex-end', p: 2, pt: 0 }}>
        {isSubscribed ? (
          <Button 
            variant="outlined" 
            color="error" 
            onClick={() => onCancel(fund.fundId)}
            size="small"
          >
            Cancelar Suscripción
          </Button>
        ) : (
          <Tooltip title={!canSubscribe ? `Saldo insuficiente. Necesita $${fund.minimumAmount.toLocaleString()} COP` : ''}>
            <span>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={() => onSubscribe(fund.fundId)}
                disabled={!canSubscribe}
                size="small"
              >
                Suscribirse
              </Button>
            </span>
          </Tooltip>
        )}
      </CardActions>
    </Card>
  );
};

export default FundCard;