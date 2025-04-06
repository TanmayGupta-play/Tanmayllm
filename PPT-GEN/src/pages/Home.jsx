import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generatePresentation } from "../api";
import Navbar from "../components/Navbar";

const Home = () => {
  const [topic, setTopic] = useState("");
  const [template, setTemplate] = useState(1);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const data = { topic, template };
      const result = await generatePresentation(data);
      console.log(result.message);
      if (result.message === "Presentation created successfully!") {
        navigate("/result");
      }
    } catch (error) {
      console.error("Error creating presentation:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-orange-900">
      {/* ✅ Navbar - Fixed at the top */}
      <div className="fixed w-full top-0 z-50">
        <Navbar />
      </div>

      {/* ✅ Main Content */}
      <div className="flex items-center justify-center min-h-screen pt-20 p-4">
        <div className="bg-white/20 backdrop-blur-lg p-8 rounded-3xl shadow-lg w-full max-w-lg border border-white/30">
          <h2 className="text-3xl font-extrabold text-center text-white">
            🎯 AI Slide Generator
          </h2>
          <p className="text-white/80 text-center mt-2">
            Create slides effortlessly with AI.
          </p>

          <form onSubmit={handleSubmit} className="space-y-6 mt-6">
            {/* ✅ Topic Input */}
            <div className="flex flex-col">
              <label className="text-white font-medium">Enter Topic:</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full mt-2 p-3 border border-white/30 rounded-lg bg-white/20 text-white placeholder-white/70 focus:ring-2 focus:ring-orange-400 outline-none"
                placeholder="e.g., Artificial Intelligence"
                required
              />
            </div>

            {/* ✅ Template Selection */}
            <div className="flex flex-col">
              <label className="text-white font-medium">Select Template:</label>
              <select
                value={template}
                onChange={(e) => setTemplate(Number(e.target.value))}
                className="w-full mt-2 p-3 border border-white/30 rounded-lg bg-gray-700 text-white focus:ring-2 focus:ring-orange-400 outline-none appearance-none"
              >
                <option value="1" className="bg-gray-800 text-white">
                  📚 Minimalistic
                </option>
                <option value="2" className="bg-gray-800 text-white">
                  🎨 Colourful
                </option>
                <option value="3" className="bg-gray-800 text-white">
                  🏢 Professional
                </option>
                <option value="4" className="bg-gray-800 text-white">
                  🌑 Dark
                </option>
              </select>
            </div>

            {/* ✅ Submit Button */}
            <button
              type="submit"
              className={`w-full mt-6 p-3 font-bold rounded-xl shadow-md transition-all duration-300 transform hover:scale-105 ${
                loading
                  ? "bg-orange-500 text-white cursor-not-allowed opacity-50"
                  : "bg-orange-500 text-white hover:bg-orange-600"
              }`}
              disabled={loading}
            >
              {loading ? "⏳ Generating..." : "🚀 Generate Presentation"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Home;
