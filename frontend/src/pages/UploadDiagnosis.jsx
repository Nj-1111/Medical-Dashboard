import React, { useState } from 'react';
import api from '../services/api';

export default function UploadDiagnosis() {
  const [file, setFile] = useState(null);
  const [patientId, setPatientId] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file || !patientId) {
      setError('Please select a file and enter patient ID');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Upload image
      const formData = new FormData();
      formData.append('file', file);
      formData.append('patient_id', patientId);

      const uploadRes = await api.post('/upload/image', formData);
      
      // Run inference
      const inferenceRes = await api.post('/inference/glaucoma', {
        patient_id: patientId,
        image_id: uploadRes.data.file_id
      });

      setResult(inferenceRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing diagnosis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Glaucoma Diagnosis</h1>

      <form onSubmit={handleSubmit} className="mb-8">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Patient ID</label>
          <input
            type="text"
            value={patientId}
            onChange={(e) => setPatientId(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
            placeholder="Enter patient ID"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Medical Image</label>
          <input
            type="file"
            onChange={handleFileChange}
            accept="image/*"
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Run Diagnosis'}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-100 text-red-700 rounded-lg mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="p-6 bg-gray-50 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">Results</h2>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-sm text-gray-600">Diagnosis</p>
              <p className="text-lg font-bold">{result.result.toUpperCase()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Confidence</p>
              <p className="text-lg font-bold">{(result.confidence_score * 100).toFixed(2)}%</p>
            </div>
          </div>
          
          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Findings</p>
            <p className="text-gray-800">{result.findings}</p>
          </div>

          <div className="mb-4">
            <p className="text-sm text-gray-600 mb-2">Recommendations</p>
            <p className="text-gray-800">{result.recommendations}</p>
          </div>

          <a
            href={result.download_link}
            className="inline-block bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Download PDF Report
          </a>
        </div>
      )}
    </div>
  );
}
