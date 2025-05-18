import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

import { loadEnv } from "vite";
import * as path from "path";

//import * as dotenv from 'dotenv';

// Load environment variables from .env file located in SummerProject root
//dotenv.config({ path: path.resolve(__dirname, '../../local.env') });

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// });

import dotenv from "dotenv";

export default defineConfig(({ mode }) => {
  const envFile =
    mode === "development" ? ".env.development" : ".env.production";
  dotenv.config({ path: envFile });

  return {
    plugins: [react()],
    build: {
      outDir: "build",
      assetsDir: "assets",
      emptyOutDir: true,
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: "http://localhost:8000", // Local backend URL
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});
