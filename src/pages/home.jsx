import React from 'react';

const Home = () => {
  const changeWallpaper = async () => {
    const response = await fetch('http://localhost:5000/change_wallpaper', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image_path: 'path_to_new_image.jpg' }) // ここで画像パスを指定
    });

    const result = await response.json();
    console.log(result.message);
  };

  return (
    <div>
      <h1>ホームページ</h1>
      <button onClick={changeWallpaper}>壁紙を変更</button>
    </div>
  );
};

export default Home;
