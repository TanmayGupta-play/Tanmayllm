import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Result from './pages/Result';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  );
};

export default App;
