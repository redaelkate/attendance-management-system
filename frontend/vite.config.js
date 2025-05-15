import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ['flexible-fine-salmon.ngrok-free.app'], // Add the blocked host here
  },
});
