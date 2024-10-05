import { useState } from 'react'
import { useNavigate, Route, Routes, BrowserRouter } from 'react-router-dom'
import Navbar from './Components/Navbar'
import HomePage from './Pages/HomePage'
import Chatbot from './Pages/Chatbot'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL
// axios.defaults.withCredentials = true


function App() {

  return (
    <BrowserRouter>

      <div className="">
        <Navbar />
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/chatbot' element={<Chatbot />} />
          {/* <Route path='/chatbotnew' element={<ChatbotNew />} /> */}
        </Routes>
      </div>
    </BrowserRouter>
  )
}
export default App
