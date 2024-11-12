import React, { useState } from 'react';
import '../animation/css/animal.css';

const Home = () => {
  const [animalSize, setAnimalSize] = useState(1.0);
  const [isVisible, setIsVisible] = useState(true);

  const changeWallpaper = async () => {
    const response = await fetch('http://localhost:5000/change_wallpaper', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image_path: 'path_to_new_image.jpg' })
    });

    const result = await response.json();
    console.log(result.message);
  };

  const updateAnimalSettings = async () => {
    const response = await fetch('http://localhost:5000/set_animal_settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ size: animalSize, is_visible: isVisible })
    });

    const result = await response.json();
    console.log(result.status, result.settings);
  };

  const handleVisibilityChange = (e) => {
    setIsVisible(e.target.checked);
    updateAnimalSettings(); // チェックが変更されたら即座にサーバーに更新を送信
  };

  return (
    <div>
      <h1>ホームページ</h1>
      <button onClick={changeWallpaper}>壁紙を変更</button>
      <img src="/kani.png" alt="Animal" className="animal" />

      <div>
        <h2>動物の設定</h2>
        <label>
          大きさ:
          <input 
            type="range" 
            min="0.5" 
            max="2.0" 
            step="0.1" 
            value={animalSize} 
            onChange={(e) => setAnimalSize(e.target.value)} 
          />
        </label>
        <span>{animalSize}</span>
        <br />
        <label>
          表示する:
          <input 
            type="checkbox" 
            checked={isVisible} 
            onChange={handleVisibilityChange} 
          />
        </label>
        <br />
        <button onClick={updateAnimalSettings}>動物の設定を更新</button>
      </div>
    </div>
  );
};

export default Home;
