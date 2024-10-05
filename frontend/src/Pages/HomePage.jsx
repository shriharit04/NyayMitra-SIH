import { FaGavel } from 'react-icons/fa'; // Replace LogoIcon
import { HiMenu } from 'react-icons/hi'; // Replace MenuIcon
import Button from '../Components/Button';
import { motion } from 'framer-motion';
import { GoLaw } from "react-icons/go";
import { SiBookstack } from "react-icons/si";
import { MdSchedule } from "react-icons/md";
import './HomePage.scss';

const features = [
  {
    icon: <MdSchedule className="h-[150px] w-auto text-purple-300" />,
    title: "Instant Judicial Guidance",
    description: "Get immediate answers to your legal queries with quick and precise guidance on various judicial matters.",
  },
  {
    icon: <MdSchedule className="h-[150px] w-auto text-purple-300" />,
    title: "Direct Lawyer Consultation",
    description: "Have lingering doubts? Connect instantly with a licensed lawyer for direct consultations right through the app.",
  },
  {
    icon: <SiBookstack className="h-[150px] w-auto text-purple-300" />,
    title: "The Ultimate Judiciary Info Hub",
    description: "Access all essential legal resources in one place, eliminating the need to sift through books and articles.",
  },
  {
    icon: <GoLaw className="h-[150px] w-auto text-purple-300" />,
    title: "Stay Updated with Trending Cases",
    description: "Keep up with the latest and most talked-about court cases in India through our regularly updated blog, ensuring you're always informed about key legal developments.",
  },
  {
    icon: <GoLaw className="h-[150px] w-auto text-purple-300" />,
    title: "KanoonGyaan",
    description: "A fun and easy-to-understand blog that breaks down basic amendments, constitutional rights, and responsibilities through gamified learning.",
  }
];

const HomePage = () => {
  return (
    <div className="home-container bg-[#121212] w-full m-0 p-0">
      {/* Hero Section */}
      <section className="h-[492px] md:h-[800px] flex items-center relative w-full p-4 md:p-8">
        {/* Purple glow */}
        <div className="absolute inset-0 bg-[radial-gradient(75%_75%_at_center_center,rgb(140,69,255,.5)_15%,rgb(14,0,36,.5)_68%,transparent)]"></div>

        {/* Planet */}
        <div className="absolute sm:h-72 sm:w-72 h-48 w-48 md:h-72 md:w-72 bg-purple-500 rounded-full border border-white/20 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-[radial-gradient(50%_50%_at_16.8%_18.3%,white,rgb(184,148,255)_37.7%,rgb(24,0,66))] shadow-[-20px_-20px_50px_rgb(255,255,255,.5),-20px_-20px_80px_rgb(255,255,255,.1),0_0_50px_rgb(140,69,255)]"></div>
        
        <div className="container relative">
          <h1 className="md:text-8xl text-5xl py-2 sm:text-6xl sm:mt-32 mt-20 w-3/4 text-transparent bg-clip-text font-semibold tracking-tighter bg-white bg-[radial-gradient(100%_100%_at_top_left,white,white,rgb(74,32,138,.5))]">Your Personal Lawyer Is Here</h1>
          <p className="text-lg text-white/70 mt-5 text-left">Simplifying the legal process, one question at a time. Get quick, reliable answers to your legal queries anytime, anywhere.</p>

          <div className="flex justify-center mt-5">
            <Button>Get Started</Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-container py-16 bg-[#100b1a] w-full">
        <h2 className="text-3xl font-bold text-center text-white mb-8">Features</h2>
        <div className="flex flex-row flex-wrap justify-center items-center gap-8 px-4 md:px-40">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="flex flex-col items-center justify-center w-full sm:w-[370px] h-[450px] bg-[#1f1f1f] p-8 rounded-lg shadow-lg gap-[10px] hover:scale-105 bg-gradient-to-br to-purple-900 from-[#121212]"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.2 }}
            >
              {feature.icon}
              <h3 className="feature-title text-2xl sm:text-4xl font-semibold text-white mt-2">{feature.title}</h3>
              <p className="feature-description text-lg text-white/70 text-left">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="footer bg-[#190D2E] text-white py-1 px-0 m-0">
        <div className="container text-center">
          <p>&copy; 2024 NyayMitra. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
