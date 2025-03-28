import React from 'react';
import { 
  List, 
  ListItem, 
  ListItemText, 
  ListItemIcon,
  ListItemSecondaryAction,
  IconButton, 
  Typography, 
  Chip, 
  Box,
  Divider
} from '@mui/material';
import FolderIcon from '@mui/icons-material/Folder';
import CancelIcon from '@mui/icons-material/Cancel';

const SubscriptionsList = ({ subscriptions, onCancel }) => {
  if (!subscriptions || subscriptions.length === 0) {
    return (
      <Typography variant="body2" sx={{ p: 2, textAlign: 'center', color: 'text.secondary' }}>
        No hay suscripciones activas.
      </Typography>
    );
  }

  return (
    <List sx={{ width: '100%' }}>
      {subscriptions.map((subscription, index) => {
        const date = new Date(subscription.subscriptionDate);
        const formattedDate = date.toLocaleDateString();

        return (
          <React.Fragment key={subscription.subscriptionId}>
            <ListItem alignItems="flex-start">
              <ListItemIcon>
                <FolderIcon color="primary" />
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="subtitle2" sx={{ mr: 1 }}>
                      {subscription.fundName || `Fondo ID: ${subscription.fundId}`}
                    </Typography>
                    <Chip
                      label={subscription.status}
                      size="small"
                      color="primary"
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
                      Monto: ${subscription.amountSubscribed.toLocaleString()} COP
                    </Typography>
                    <Typography
                      component="div"
                      variant="caption"
                      color="text.secondary"
                    >
                      Suscrito desde: {formattedDate}
                    </Typography>
                  </>
                }
              />
              <ListItemSecondaryAction>
                <IconButton 
                  edge="end" 
                  aria-label="cancel" 
                  onClick={() => onCancel(subscription.fundId)}
                  color="error"
                  size="small"
                >
                  <CancelIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
            {index < subscriptions.length - 1 && <Divider variant="inset" component="li" />}
          </React.Fragment>
        );
      })}
    </List>
  );
};

export default SubscriptionsList;