import React, { useState } from 'react';
import axios from 'axios';
import './HomePage.css';

function HomePage() {
  const [responseData, setResponseData] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleButtonClick = () => {
    const url = 'http://localhost:5000/api/moonboard_get_top_n?N=10';
    axios.get(url)
      .then(response => {
        console.log(response.data);
        setResponseData(JSON.stringify(response.data, null, 2));
        setShowModal(true);
      })
      .catch(error => {
        console.log(error);
      });
  };
    
  return (
    <div>
      <div className="button-container">
        <button className="Login">Login</button>
        <button className="Sign Up">Signup</button>
        <button className="Test Button" onClick={handleButtonClick}>Test Button</button>
      </div>
      <h1 id="homepage-title">Moonboard</h1>
      <p className="redesigned">Redesigned and Improved</p>
      {showModal && (
        <div className="modal">
          <div className={`modal-content ${responseData ? 'modal-content-white' : ''}`}>
            <button onClick={() => setShowModal(false)}>Close</button>
            <p>{responseData}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;

