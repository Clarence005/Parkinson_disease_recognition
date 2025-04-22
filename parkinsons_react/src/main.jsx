import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './components/App.jsx'
import './style/index.css'  // ✅ Important: matches your folder structure

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
