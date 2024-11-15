import React, { useState } from 'react';
// import '../animation/css/animal.css';

const View = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [animalSize, setAnimalSize] = useState(1.0);  // 新しいサイズの状態を追加

  // 動物の表示設定をサーバーに送信する関数
  const updateAnimalSettings = async () => {
    const response = await fetch('http://localhost:5000/set_animal_settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ is_visible: isVisible, size: animalSize }) // sizeも送信
    });

    const result = await response.json();
    console.log(result.status, result.settings);
  };

  // チェックボックスの変更を処理
  const handleVisibilityChange = (e) => {
    setIsVisible(e.target.checked);
    updateAnimalSettings();  // 表示状態をサーバーに即時送信
  };

  // サイズ入力の変更を処理
  const handleSizeChange = (e) => {
    setAnimalSize(e.target.value);
  };

  return (
    <div>
      <h1>ホームページ</h1>
      <label>
        表示する:
        <input 
          type="checkbox" 
          checked={isVisible} 
          onChange={handleVisibilityChange} 
        />
      </label>
      <div>
        <label>
          画像の大きさ:
          <input 
            type="number" 
            min="0.5" 
            max="3.0" 
            step="0.1" 
            value={animalSize} 
            onChange={handleSizeChange} 
          />
        </label>
        <button onClick={updateAnimalSettings}>サイズを更新</button>
      </div>
    </div>
  );
};

export default View;
