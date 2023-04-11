import React, { useState } from 'react';
import './HomePage.css';
import { URL } from 'url';
import http from 'http';


function HomePage(props) {
  const [responseData, setResponseData] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleButtonClick = () => {
    const url = 'http://localhost:5000/get_routes_from_list?user_id=1&list_name=test_list';
    props.axiosInstance.get(url)
      .then(response => {
        setResponseData(response.data);
        setShowModal(true);
      })
      .catch(error => {
        console.log(error);
      });
  };
    
  return (
    <div>
      <div className="button-container">
        <button className="Login">Button 1</button>
        <button className="Sign Up">Button 2</button>
        <button className="Test Button" onClick={handleButtonClick}>Test Button</button>
      </div>
      <h1 style={styles.h1}>Moonboard</h1>
      <p style={styles.p}>Redesigned and Improved</p>
      {showModal && (
        <div className="modal">
          <div className="modal-content">
            <button onClick={() => setShowModal(false)}>Close</button>
            <p>{responseData}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomePage;
