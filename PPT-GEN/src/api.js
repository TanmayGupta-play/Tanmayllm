// src/api/index.js

const API_URL = 'http://localhost:5000/api';

/**
 * Generate a presentation with the given data
 * @param {Object} data - The presentation data
 * @param {string} data.topic - The presentation topic
 * @param {number} data.template - The template ID (1-4)
 * @param {boolean} data.includeCode - Whether to include code examples
 * @returns {Promise<Object>} The API response
 */
export const generatePresentation = async (data) => {
  try {
    const response = await fetch(`${API_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to generate presentation');
    }

    return await response.json();
  } catch (error) {
    console.error('Error in generatePresentation:', error);
    throw error;
  }
};

/**
 * Get information about the current presentation
 * @returns {Promise<Object>} The presentation information
 */
export const getResultInfo = async () => {
  try {
    const response = await fetch(`${API_URL}/result`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to get presentation info');
    }

    return await response.json();
  } catch (error) {
    console.error('Error in getResultInfo:', error);
    throw error;
  }
};

/**
 * Get the download URL for a presentation
 * @param {string} presentationId - The presentation ID
 * @returns {string} The download URL
 */
export const getDownloadUrl = (presentationId) => {
  return `${API_URL}/download/${presentationId}`;
};

export default {
  generatePresentation,
  getResultInfo,
  getDownloadUrl
};