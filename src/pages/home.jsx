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
      <button class="btn1" onClick={handleLogin}>ログイン</button>
      <button class="btn2">使い方</button>
    </div>
  );
}

export default Home;
