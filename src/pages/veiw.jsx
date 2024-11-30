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
      //setFeedbackMessage('エラーが発生しました。設定を保存できませんでした。');
      console.error("ネットワークエラー:", error);
    }
  };

  // 表示設定の変更時に処理
  const handleVisibilityChange = (e) => {
    const newVisibility = e.target.checked;
    setIsVisible(newVisibility);
    updateAnimalSettings({ is_visible: newVisibility, size: animalSize }); // 即時送信
  };



  return (
  
      <div className="view-container">
      <div className="layout">
      <div class="inputGroup">
    <input id="option1" name="option1" type="checkbox"/>
    <label for="option1">Windows表示　</label>
  </div>
  <link href="https://fonts.googleapis.com/css?family=Fira+Sans" rel="stylesheet"></link>

    <div className="video-container">
      <video width="100%" height="100%" autoPlay loop muted>
        <source src="videos/test.mp4" type="video/mp4" />
        お使いのブラウザは動画タグに対応していません。
      </video>
    </div>

      {/* フィードバックメッセージ */}
      {feedbackMessage && <p>{feedbackMessage}</p>}
      </div>
    </div>
  );
};

export default View;
