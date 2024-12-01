import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/home.css';

const Home = () => {

  const navigate = useNavigate()

  const handleLogin = () => {
    navigate('/select')
  }

  return (
    <div className="container">
      <h1>VirtuPet</h1>
      <button className="btn1" onClick={handleLogin}>
        はじめる
      </button>
    </div>
  );
}

export default Home;
