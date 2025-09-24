import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Auth0Provider } from '@auth0/auth0-react'
import { auth0Config } from './config/auth0.js'
import ErrorBoundary from './components/ErrorBoundary.jsx'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <Auth0Provider {...auth0Config}>
        <App />
      </Auth0Provider>
    </ErrorBoundary>
  </StrictMode>,
)
