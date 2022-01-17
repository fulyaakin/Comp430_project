import React, { useEffect, useState } from "react";
import './App.css';
import Login from './screens/Login'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from './components/ProtectedRoute'
import Homepage from "./screens/Homepage";
import axios from "axios";

function App() {

  return (
    <BrowserRouter>
          <div className="container">
            <Routes>
              <Route path="/" element={<Login/>} />
              <Route path="/home" element={<Homepage/>} />
            </Routes>
          </div>
      </BrowserRouter>
  );
}

export default App;
