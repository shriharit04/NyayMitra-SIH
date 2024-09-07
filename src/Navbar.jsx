// src/Navbar.js
import React from 'react';
import mainLogo from './meowmeow.png';
import './Navbar.css';

function Navbar() {
  return (
    <div className="navbar">
      <section>
      <div className="logo">
        <img src={mainLogo} alt="fireSpot"/>
      </div>
      </section>
      <nav className="nav-links">
        <ul>
          <li><a href="https://doj.gov.in/">Home</a></li>
          <li><a href="https://doj.gov.in/about-department/">About</a></li>
          <li><a href="https://doj.gov.in/organization-chart/">Features</a></li>
          <li><a href="https://doj.gov.in/contact-us/">Contact</a></li>
        </ul>
      </nav>
    </div>
  );
}

export default Navbar;