import React from 'react';
import { 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon, 
  Typography, 
  Chip, 
  Box,
  Divider
} from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';

const TransactionHistory = ({ transactions }) => {
  if (!transactions || transactions.length === 0) {
    return (
      <Typography variant="body2" sx={{ p: 2, textAlign: 'center', color: 'text.secondary' }}>
        No hay transacciones para mostrar.
      </Typography>
    );
  }

  return (
    <List sx={{ width: '100%' }}>
      {transactions.map((transaction, index) => {
        const isSubscription = transaction.type === 'SUBSCRIPTION';
        const date = new Date(transaction.transactionDate);
        const formattedDate = `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;

        return (
          <React.Fragment key={transaction.transactionId}>
            <ListItem alignItems="flex-start">
              <ListItemIcon>
                {isSubscription ? (
                  <AddCircleOutlineIcon color="success" />
                ) : (
                  <RemoveCircleOutlineIcon color="error" />
                )}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="subtitle2">
                      {transaction.fundName || `Fondo ID: ${transaction.fundId}`}
                    </Typography>
                    <Chip
                      label={isSubscription ? 'Suscripción' : 'Cancelación'}
                      size="small"
                      color={isSubscription ? 'success' : 'error'}
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={
                  <>
                    <Typography
                      component="span"
                      variant="body2"
                      color="text.primary"
                    >
                      ${transaction.amount.toLocaleString()} COP
                    </Typography>
                    <Typography
                      component="div"
                      variant="caption"
                      color="text.secondary"
                    >
                      {formattedDate}
                    </Typography>
                  </>
                }
              />
            </ListItem>
            {index < transactions.length - 1 && <Divider variant="inset" component="li" />}
          </React.Fragment>
        );
      })}
    </List>
  );
};

export default TransactionHistory;