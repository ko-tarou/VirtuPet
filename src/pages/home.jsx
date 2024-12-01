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
      <h1 className='title'>VirtuPet</h1>
      <button className="btn1" onClick={handleLogin}>ログイン</button>
    </div>
  );
}

export default Home;
