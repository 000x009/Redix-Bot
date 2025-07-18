import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { init } from './init';
import App from './App';


const root = ReactDOM.createRoot(document.getElementById('root'));

await init()

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
