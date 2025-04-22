import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Loginpage from './pages/LoginPage';
import Home from './pages/Home';
import Spiral from './phases/Spiral';
import Bradykinesia from './phases/Bradykinesia';
import Tremors from './phases/Tremors';
import Gait from './phases/Gait';
import PrivateRoute from './pages/PrivateRoute';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Loginpage />} />
        <Route path="/home" element={<PrivateRoute><Home /></PrivateRoute>} />
        <Route path="/spiral" element={<PrivateRoute><Spiral /></PrivateRoute>} />
        <Route path="/bradykinesia" element={<PrivateRoute><Bradykinesia /></PrivateRoute>} />
        <Route path="/tremors" element={<PrivateRoute><Tremors /></PrivateRoute>} />
        <Route path="/gait" element={<PrivateRoute><Gait /></PrivateRoute>} />
      </Routes>
    </Router>
  );
}
