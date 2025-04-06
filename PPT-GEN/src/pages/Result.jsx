// src/pages/Result.jsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getResultInfo, getDownloadUrl } from '../api';
import Navbar from '../components/Navbar';

const Result = () => {
  const [presentationInfo, setPresentationInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPresentationInfo = async () => {
      try {
        const info = await getResultInfo();
        setPresentationInfo(info);
      } catch (err) {
        console.error('Error fetching presentation info:', err);
        setError('Could not load presentation information. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchPresentationInfo();
  }, []);

  const handleCreateAnother = () => {
    navigate('/');
  };

  if (loading) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-orange-900">
        <div className="fixed w-full top-0 z-50">
          <Navbar />
        </div>
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-white text-2xl">Loading your presentation...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="relative min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-orange-900">
        <div className="fixed w-full top-0 z-50">
          <Navbar />
        </div>
        <div className="flex items-center justify-center min-h-screen">
          <div className="bg-white/20 backdrop-blur-lg p-8 rounded-3xl shadow-lg w-full max-w-lg border border-white/30">
            <h2 className="text-3xl font-extrabold text-center text-white">Error</h2>
            <p className="text-white/80 text-center mt-4">{error}</p>
            <button
              onClick={handleCreateAnother}
              className="w-full mt-6 p-3 font-bold rounded-xl shadow-md transition-all duration-300 transform hover:scale-105 bg-orange-500 text-white hover:bg-orange-600"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-orange-900">
      <div className="fixed w-full top-0 z-50">
        <Navbar />
      </div>

      <div className="flex items-center justify-center min-h-screen pt-20 p-4">
        <div className="bg-white/20 backdrop-blur-lg p-8 rounded-3xl shadow-lg w-full max-w-lg border border-white/30">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-orange-500 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
          </div>

          <h2 className="text-3xl font-extrabold text-center text-white">Success!</h2>
          <p className="text-white/80 text-center mt-2 mb-6">
            Your presentation has been generated successfully.
          </p>

          <div className="flex flex-col space-y-4">
            <a
              href={getDownloadUrl(presentationInfo.presentation_id)}
              className="w-full p-3 font-bold rounded-xl shadow-md text-center transition-all duration-300 transform hover:scale-105 bg-orange-500 text-white hover:bg-orange-600"
              download
            >
              Download Presentation
            </a>

            <button
              onClick={handleCreateAnother}
              className="w-full p-3 font-bold rounded-xl shadow-md transition-all duration-300 transform hover:scale-105 bg-white/30 text-white hover:bg-white/40"
            >
              Create Another Presentation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Result;