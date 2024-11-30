import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/Instructions.css';

const Instructions = () => {

  const navigate = useNavigate()

  const handleLogin = () => {
    navigate('/select')
  }

  return (
    <div className="container-instructions">
      <h1>VirtuPetの使い方</h1>
      <p className="description">
        VirtuPetは、仮想ペットを鑑賞できるアプリケーションです。<br />
        ペットを鑑賞し、癒されましょう。<br />
        さっそく、ペットを選んでみましょう。<br />
        </p>
      <button class="btn1" onClick={handleLogin}>ログイン</button>
    </div>
  );
}

export default Instructions;
