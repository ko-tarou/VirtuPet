import React from 'react';
import { Link } from 'react-router-dom';
import '../pages/styles/Header.css';

const Header = () => {
  return (
    <header className="header">
      <h1>VirtuPet</h1>
      <nav>
        <ul className="nav-links">
          <li><Link to="/">ホーム</Link></li>
          <li><Link to="/select">ペット選択</Link></li>
          <li><Link to="/view">ペット閲覧</Link></li>
          <li><Link to="/instructions">使い方</Link></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;