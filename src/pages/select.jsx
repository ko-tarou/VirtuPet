import React from 'react';
import '../pages/styles/select.css';

const Select = () => {

  return (
    <div className="container-select">
        <div className="button-container">
            <img src="path/to/fox-image.jpg" alt="きつね" className="button-image" />
            <button className="chara1">きつね</button>
        </div>
        <div className="button-container">
            <img src="path/to/dog-image.jpg" alt="いぬ" className="button-image" />
            <button className="chara2">いぬ</button>
        </div>
        <div className="button-container">
            <img src="path/to/rabbit-image.jpg" alt="うさぎ" className="button-image" />
            <button className="chara3">うさぎ</button>
        </div>
    </div>
  );
}

export default Select;