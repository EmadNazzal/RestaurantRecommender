import "@testing-library/jest-dom";

global.importMetaEnv = {
  VITE_GOOGLE_MAPS_API_KEY: "fake-api-key",
  VITE_GOOGLE_MAPS_ID_KEY: "fake-map-id",
};

Object.defineProperty(global, "import", {
  value: { meta: { env: global.importMetaEnv } },
});
