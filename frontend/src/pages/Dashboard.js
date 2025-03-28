import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  Container, 
  Typography, 
  Grid, 
  Paper, 
  Box, 
  Divider, 
  Alert, 
  Snackbar, 
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import FundCard from '../components/FundCard';
import TransactionHistory from '../components/TransactionHistory';
import SubscriptionsList from '../components/SubscriptionsList';
import ClientBalance from '../components/ClientBalance';
import { fetchClientInfo } from '../store/slices/clienteSlice';
import { fetchAllFunds } from '../store/slices/fondoSlice';
import { 
  fetchActiveSubscriptions, 
  fetchTransactionHistory,
  subscribeToFundAction,
  cancelFundSubscription,
  clearError,
  clearLastOperation
} from '../store/slices/transaccionSlice';

const Dashboard = () => {
  const dispatch = useDispatch();
  const [alertMessage, setAlertMessage] = useState('');
  const [alertSeverity, setAlertSeverity] = useState('info');
  const [openAlert, setOpenAlert] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  
  const { clientInfo, loading: clientLoading, error: clientError } = useSelector(state => state.cliente);
  const { fundsList, loading: fundsLoading, error: fundsError } = useSelector(state => state.fondo);
  const { 
    activeSubscriptions, 
    transactions, 
    loading: transactionLoading,
    error: transactionError,
    lastOperation
  } = useSelector(state => state.transaccion);
  
  // Cargar datos al iniciar
  useEffect(() => {
    dispatch(fetchClientInfo());
    dispatch(fetchAllFunds());
    dispatch(fetchActiveSubscriptions());
    dispatch(fetchTransactionHistory());
  }, [dispatch]);
  
  // Mostrar errores si ocurren
  useEffect(() => {
    const errorMessage = clientError || fundsError || transactionError;
    if (errorMessage) {
      // Asegurarse de que el mensaje de error sea una cadena
      const errorText = typeof errorMessage === 'object' 
        ? JSON.stringify(errorMessage) 
        : String(errorMessage);
      
      setAlertMessage(errorText);
      setAlertSeverity('error');
      setOpenAlert(true);
    }
  }, [clientError, fundsError, transactionError]);
  
  // Manejar resultado de operaciones
  useEffect(() => {
    if (lastOperation) {
      if (lastOperation.success) {
        setAlertMessage(
          lastOperation.type === 'SUBSCRIPTION' 
            ? 'Suscripción exitosa al fondo - mensaje enviado' 
            : 'Cancelación exitosa de la suscripción - mensaje enviado'
        );
        setAlertSeverity('success');
      } else {
        // Asegurarse de que el mensaje de error sea una cadena
        const errorText = typeof lastOperation.error === 'object' 
          ? JSON.stringify(lastOperation.error) 
          : String(lastOperation.error || `Error en operación de ${lastOperation.type}`);
        
        setAlertMessage(errorText);
        setAlertSeverity('error');
      }
      setOpenAlert(true);
      
      // Actualizar datos después de una operación exitosa
      if (lastOperation.success) {
        dispatch(fetchClientInfo());
        dispatch(fetchActiveSubscriptions());
        dispatch(fetchTransactionHistory());
      }
      
      // Limpiar el estado de la operación
      setTimeout(() => {
        dispatch(clearLastOperation());
      }, 1000);
    }
  }, [lastOperation, dispatch]);
  
  const handleSubscribe = async (fundId) => {
    dispatch(subscribeToFundAction(fundId));
  };
  
  const handleCancelSubscription = async (fundId) => {
    dispatch(cancelFundSubscription(fundId));
  };
  
  const handleCloseAlert = () => {
    setOpenAlert(false);
    dispatch(clearError());
  };
  
  const handleChangeTab = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  // Verificar si un fondo tiene suscripción activa
  const isSubscribed = (fundId) => {
    return activeSubscriptions?.some(sub => sub.fundId === fundId);
  };
  
  if (clientLoading || fundsLoading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Información del Cliente y Saldo */}
      <ClientBalance clientInfo={clientInfo || {}} />
      
      <Grid container spacing={4}>
        {/* Panel izquierdo: Fondos Disponibles */}
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 3, height: '100%', borderRadius: 2, boxShadow: 3 }}>
            <Typography variant="h5" gutterBottom>
              Fondos Disponibles
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            {fundsList && fundsList.length > 0 ? (
              fundsList.map(fund => (
                <FundCard 
                  key={fund.fundId}
                  fund={fund}
                  onSubscribe={handleSubscribe}
                  onCancel={handleCancelSubscription}
                  isSubscribed={isSubscribed(fund.fundId)}
                  clientBalance={clientInfo?.balance || 0}
                />
              ))
            ) : (
              <Typography sx={{ p: 2, textAlign: 'center', color: 'text.secondary' }}>
                No hay fondos disponibles o hubo un error al cargarlos.
              </Typography>
            )}
          </Paper>
        </Grid>
        
        {/* Panel derecho: Tabs para Suscripciones e Historial */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ borderRadius: 2, boxShadow: 3 }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs 
                value={activeTab} 
                onChange={handleChangeTab} 
                variant="fullWidth"
                sx={{ minHeight: 48 }}
              >
                <Tab label="Suscripciones Activas" id="tab-0" />
                <Tab label="Historial de Transacciones" id="tab-1" />
              </Tabs>
            </Box>
            
            <Box sx={{ p: 2 }}>
              {activeTab === 0 && (
                <Box>
                  <SubscriptionsList 
                    subscriptions={activeSubscriptions || []} 
                    onCancel={handleCancelSubscription} 
                  />
                </Box>
              )}
              
              {activeTab === 1 && (
                <Box>
                  {transactionLoading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                      <CircularProgress size={24} />
                    </Box>
                  ) : (
                    <TransactionHistory transactions={transactions || []} />
                  )}
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
      
      <Snackbar 
        open={openAlert} 
        autoHideDuration={6000} 
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert 
          onClose={handleCloseAlert} 
          severity={alertSeverity} 
          sx={{ width: '100%' }}
          variant="filled"
        >
          {alertMessage}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Dashboard;