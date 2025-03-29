module.exports = {
    collectCoverageFrom: [
      "src/**/*.{js,jsx}",
      "!src/index.js",
      "!src/reportWebVitals.js"
    ],
    coverageThreshold: {
      global: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80
      }
    },
    testEnvironment: "jsdom",
    transform: {
      "^.+\\.(js|jsx)$": "babel-jest"
    },
    transformIgnorePatterns: [
      "/node_modules/(?!(axios)/)"
    ],
    moduleNameMapper: {
      "\\.(css|less|scss|sass)$": "<rootDir>/src/__mocks__/styleMock.js",
      "\\.(jpg|jpeg|png|gif|svg)$": "<rootDir>/src/__mocks__/fileMock.js"
    },
    setupFilesAfterEnv: [
      "<rootDir>/src/setupTests.js"
    ]
  };