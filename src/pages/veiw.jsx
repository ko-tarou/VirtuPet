import React, { useState } from 'react';
import '../pages/styles/veiw.css'; // CSSファイルをインポート

const View = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [animalSize, setAnimalSize] = useState(1.0);
  const [feedbackMessage, setFeedbackMessage] = useState('');

  // 動物の設定をサーバーに送信する関数
  const updateAnimalSettings = async (settings) => {
    try {
      const response = await fetch('http://localhost:5000/set_animal_settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings)
      });

      if (response.ok) {
        const result = await response.json();
        setFeedbackMessage(`設定を更新しました: ${JSON.stringify(result.settings)}`);
        console.log("設定がサーバーに送信されました:", result.settings);
      } else {
        const errorResult = await response.json();
        setFeedbackMessage(`エラー: ${errorResult.message}`);
        console.error("サーバーエラー:", errorResult.message);
      }
    } catch (error) {
      setFeedbackMessage('エラーが発生しました。設定を保存できませんでした。');
      console.error("ネットワークエラー:", error);
    }
  };

  // 表示設定の変更時に処理
  const handleVisibilityChange = (e) => {
    const newVisibility = e.target.checked;
    setIsVisible(newVisibility);
    updateAnimalSettings({ is_visible: newVisibility, size: animalSize }); // 即時送信
  };

  // サイズ変更時に処理
  const handleSizeChange = (e) => {
    const newSize = parseFloat(e.target.value);
    setAnimalSize(newSize);
    updateAnimalSettings({ is_visible: isVisible, size: newSize }); // 即時送信
  };

  return (
    <div>
      <div class="view-container">
      <div class="layout">
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
      </div>
      
      {/* プレビュー用の動物画像 */}
      <div 
        style={{
          width: `${animalSize * 100}px`,
          height: `${animalSize * 100}px`,
          backgroundImage: 'url(/path/to/animal.png)', // プレビュー画像のパスを指定
          backgroundSize: 'contain',
          backgroundRepeat: 'no-repeat',
          display: isVisible ? 'block' : 'none',
          marginTop: '20px',
          border: '1px solid #ccc' // プレビュー枠の視認性向上
        }}
      ></div>
      </div>
      <div className="center-screen">
      <div className="game-screen">
        {/* ゲーム画面のコンテンツをここに追加 */}
      </div>
    </div>

      {/* フィードバックメッセージ */}
      {feedbackMessage && <p>{feedbackMessage}</p>}
      </div>
    </div>
  );
};

export default View;
