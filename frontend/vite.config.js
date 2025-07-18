import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc';
import mkcert from 'vite-plugin-mkcert';

export default defineConfig({
  plugins: [
    react(),
    mkcert()
  ],
  server: {
    https: true,
    host: true,
  },
  assetsInclude: ['**/*.PNG'],
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  },
  publicDir: 'public'
})
