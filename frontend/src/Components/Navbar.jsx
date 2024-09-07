// Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
const Navbar = () => {
  return (
    <div className='flex mt-1 items-center justify-between bg-black text-white p-4 w-auto rounded-xl mb-4'>
      <Link to='/'>
        <div className='flex items-center '>
          NyayMitra
        </div>
      </Link>
      <div className=''>
        <Link to="/chatbot" className='mr-2 hover:bg-gray-100 hover:text-secondary hover:underline p-2 border-stone-100 rounded-lg'>Chat Now</Link>
      </div>
    </div>
  )
};



export default Navbar;
