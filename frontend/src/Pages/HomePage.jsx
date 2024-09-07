import React from 'react';
import { motion } from 'framer-motion';
import HeroIcon from '../assets/HomePage/heroIcon.svg'; //put logo
import { GoLaw } from "react-icons/go";
import { SiBookstack } from "react-icons/si";

import { MdSchedule } from "react-icons/md";

import './HomePage.scss';

const features = [
  {
    icon: <MdSchedule className="feature-icon" />,
    title: "Instant Judicial Guidance",
    description: "Get immediate answers to your legal queries with quick and precise guidance on various judicial matters.",
  },
  {
    icon: <MdSchedule className="feature-icon" />,
    title: "Direct Lawyer Consultation",
    description: "Have lingering doubts? Connect instantly with a licensed lawyer for direct consultations right through the app.",
  },
  {
    icon: <SiBookstack className="feature-icon" />,
    title: "The Ultimate Judiciary Info Hub",
    description: "Access all essential legal resources in one place, eliminating the need to sift through books and articles.",
  },
  {
    icon: <GoLaw className="feature-icon" />,
    title: "Stay Updated with Trending Cases",
    description: "Keep up with the latest and most talked-about court cases in India through our regularly updated blog, ensuring you're always informed about key legal developments.",
  },
  {
    icon: <GoLaw className="feature-icon" />,
    title: "KanoonGyaan",
    description: "A fun and easy-to-understand blog that breaks down basic amendments, constitutional rights, and responsibilities through gamified learning.",
  }
];

const HomePage = () => {
  return (
    <div className="home-container">
      {/* Hero Section */}
      <section className="hero-section">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="hero-title">Welcome to NyayMitra</h1>
          <p className="hero-description">Your trusted legal assistant</p>
          <div className="button-container">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="button"
            >
              AI Assistant
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="button"
            >
              Book a Lawyer
            </motion.button>
          </div>
        </motion.div>
        <img src={HeroIcon} alt="Hero Icon" />
      </section>

      {/* Features Section */}
      <section id="features" className="features-container">
        <h2 className="text-3xl font-bold mb-8">Features</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="featureh"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.2 }}
            >
              {feature.icon}
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>&copy; 2024 NyayMitra. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default HomePage;
