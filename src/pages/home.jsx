import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>ホームページ</h1>
      <Link to="/login">Go to Login</Link>
    </div>
  );
};

export default Home;
