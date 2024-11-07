import React from 'react';
import "../animetion/animal.css";

const Home = () => {
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

  return (
    <div>
      <h1>ホームページ</h1>
      <button onClick={changeWallpaper}>壁紙を変更</button>
      <img src="/kani.png" alt="Animal" className="animal" />
    </div>
  );
};

export default Home;
