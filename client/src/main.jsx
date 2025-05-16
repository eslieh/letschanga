import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import HeroSection from './pages/HeroSection.jsx';
import AuthFlow from './pages/Auth.jsx';
import FundraiserPage from './pages/fundraiser.jsx';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import PrivateRoute from './components/PrivateRoute';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HeroSection />} />
        <Route path="/auth" element={<AuthFlow />} />
        <Route path='/fundraiser' element={<FundraiserPage/>} />
        <Route
          path="/app"
          element={
            <PrivateRoute>
              <App />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
    <ToastContainer position="top-right" autoClose={3000} />
  </StrictMode>
);
