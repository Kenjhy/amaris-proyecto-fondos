// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Configuración global para las pruebas
global.console = {
  ...console,
  // Desactivar logs específicos durante las pruebas para mantener la salida limpia
  error: jest.fn(),
  warn: jest.fn(),
  // Mantener el log para debugging
  log: console.log,
};
