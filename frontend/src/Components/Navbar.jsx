// Navbar.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaGavel } from 'react-icons/fa';
import { HiMenu } from 'react-icons/hi';
import Button from '../Components/Button';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false); // State to control menu visibility

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className='fixed w-full flex justify-center items-center z-[50] bg-[#190D2E] top-0 bg-transparent backdrop-blur-md'>
      <div className="my-4 border-b border-white/15 md:border-none w-2/3">
        <div className="container">
          <div className="flex justify-between items-center md:border border-white/15 md:p-2.5 rounded-xl max-w-2xl mx-auto">
            {/* Logo Section */}
            <Link to="/" className='border h-16 w-16 rounded-lg inline-flex justify-center items-center border-white/15 ml-8'>
              <FaGavel className='h-full w-full text-white' />
            </Link>

            {/* Navigation Links */}
            <div className='hidden md:block'>
              <nav className='flex gap-8 text-sm'>
                <Link to='#features' className='text-white/70 hover:text-white transition'>Features</Link>
                <Link to="/contact" className='text-white/70 hover:text-white transition'>Contact</Link>
              </nav>
            </div>

            {/* Chat Button and Menu Icon */}
            <div className='flex gap-4 items-center mr-4'>
              <Link to="/chatbot">
                <Button>Chat Now</Button>
              </Link>
              <HiMenu className='md:hidden h-6 w-6 text-white cursor-pointer' onClick={toggleMenu} />
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className='md:hidden bg-[#190D2E] absolute top-full left-0 w-full border-t border-white/15'>
          <nav className='flex flex-col items-center py-4'>
            <Link to='#features' className='text-white/70 hover:text-white transition mb-2'>Features</Link>
            <Link to="/contact" className='text-white/70 hover:text-white transition mb-2'>Contact</Link>
          </nav>
        </div>
      )}
    </header>
  );
};

export default Navbar;
