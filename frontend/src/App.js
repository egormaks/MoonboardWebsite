import React from 'react';
import axios from 'axios';
import './App.css';
import HomePage from './components/HomePage';

function App() {
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000' // your backend API endpoint
  });
  const backgroundColor = '#121212';
  return (
    <div className="App" style={{ backgroundColor, height: '100%' }}>
      <HomePage axios={axiosInstance} />
    </div>
  );
}

export default App;

