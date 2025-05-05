import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App.jsx'
import HeroSection from './pages/HeroSection.jsx';
import AuthFlow from './pages/Auth.jsx';
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route element={<HeroSection/>} path="/"></Route>
        <Route element={<AuthFlow/>} path='/auth'></Route>
        <Route element={<App/>} path="/app"></Route>
      </Routes>
    </Router>
  </StrictMode>,
)
