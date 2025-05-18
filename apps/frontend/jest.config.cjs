module.exports = {
  testEnvironment: "jest-environment-jsdom",
  moduleFileExtensions: ["js", "jsx"],
  testMatch: ["**/?(*.)+(test).[jt]s?(x)"],
  transform: {
    "^.+\\.jsx?$": "babel-jest",
  },
  moduleNameMapper: {
    "\\.(css|less)$": "identity-obj-proxy",
    "\\.(png|jpg|jpeg|gif|svg)$": "identity-obj-proxy",
  },
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
};
