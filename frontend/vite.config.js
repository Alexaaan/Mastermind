import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../backend/static', // copie le build React directement dans FastAPI
    emptyOutDir: true,
  }
});
