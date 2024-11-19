import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import View from './pages/veiw';
import Select from './pages/select';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/view" element={<View/>}/>
        <Route path="/select" element={<Select/>}/>
      </Routes>
    </Router>
  );
};

export default App;
