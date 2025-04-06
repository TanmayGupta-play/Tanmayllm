import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-indigo-500 to-blue-500 p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <Link
          to="/"
          className="text-white text-2xl font-bold tracking-wide hover:text-gray-200"
        >
          🎯 PPT Generator
        </Link>
        <div className="space-x-6">
          <Link
            to="/"
            className="text-white hover:text-gray-300 font-medium transition duration-200"
          >
            Home
          </Link>
          <Link
            to="/result"
            className="text-white hover:text-gray-300 font-medium transition duration-200"
          >
            Results
          </Link>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-white hover:text-gray-300 font-medium transition duration-200"
          >
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
