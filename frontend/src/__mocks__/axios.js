const axios = {
    create: jest.fn(() => axios),
    get: jest.fn(() => Promise.resolve({ data: {} })),
    post: jest.fn(() => Promise.resolve({ data: {} })),
    put: jest.fn(() => Promise.resolve({ data: {} })),
    delete: jest.fn(() => Promise.resolve({ data: {} })),
    patch: jest.fn(() => Promise.resolve({ data: {} })),
    defaults: {
      baseURL: '',
      headers: {
        'Content-Type': 'application/json'
      }
    }
  };
  
  module.exports = axios;