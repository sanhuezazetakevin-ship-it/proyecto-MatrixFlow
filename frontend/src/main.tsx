<<<<<<< HEAD
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
=======
import { StrictMode }
  from "react";

import { createRoot }
  from "react-dom/client";

import { BrowserRouter }
  from "react-router-dom";

import App from "./App";

import { AuthProvider }
  from "./context/AuthContext";

import "./index.css";


createRoot(
  document.getElementById("root")!
).render(
  <StrictMode>

    <BrowserRouter>

      <AuthProvider>

        <App />

      </AuthProvider>

    </BrowserRouter>

  </StrictMode>
);
>>>>>>> 87884f86cb2298dcd4e88163aca4349d473a1149
