import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function Dashboard() {
  const [models, setModels] = useState(null);
  const [newGlaucomaModel, setNewGlaucomaModel] = useState('');
  const [newLLMModel, setNewLLMModel] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchModelStatus();
  }, []);

  const fetchModelStatus = async () => {
    try {
      const res = await api.get('/inference/models/status');
      setModels(res.data);
    } catch (err) {
      console.error('Error fetching models:', err);
    }
  };

  const switchGlaucomaModel = async () => {
    if (!newGlaucomaModel) return;
    
    setLoading(true);
    try {
      await api.post('/inference/models/switch-glaucoma', null, {
        params: { model_name: newGlaucomaModel }
      });
      setNewGlaucomaModel('');
      await fetchModelStatus();
    } catch (err) {
      alert('Error switching model: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  const switchLLMModel = async () => {
    if (!newLLMModel) return;
    
    setLoading(true);
    try {
      await api.post('/inference/models/switch-llm', null, {
        params: { model_name: newLLMModel }
      });
      setNewLLMModel('');
      await fetchModelStatus();
    } catch (err) {
      alert('Error switching model: ' + err.response?.data?.detail);
    } finally {
      setLoading(false);
    }
  };

  if (!models) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      {/* Model Status */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Glaucoma Detection Model</h3>
          <p className="text-gray-600 mb-2"><strong>Model:</strong> {models.glaucoma_model}</p>
          <p className="text-gray-600 mb-2"><strong>Version:</strong> {models.glaucoma_model_version}</p>
          <p className="text-gray-600"><strong>Status:</strong> <span className={models.glaucoma_model_loaded ? 'text-green-600' : 'text-red-600'}>
            {models.glaucoma_model_loaded ? '✓ Loaded' : '✗ Not Loaded'}
          </span></p>
        </div>

        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">LLM Model</h3>
          <p className="text-gray-600 mb-2"><strong>Model:</strong> {models.llm_model}</p>
          <p className="text-gray-600 mb-2"><strong>Version:</strong> {models.llm_model_version}</p>
          <p className="text-gray-600"><strong>Status:</strong> <span className={models.llm_model_loaded ? 'text-green-600' : 'text-red-600'}>
            {models.llm_model_loaded ? '✓ Loaded' : '✗ Not Loaded'}
          </span></p>
        </div>
      </div>

      {/* Switch Models */}
      <div className="grid grid-cols-2 gap-6">
        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Switch Glaucoma Model</h3>
          <div className="mb-4">
            <input
              type="text"
              value={newGlaucomaModel}
              onChange={(e) => setNewGlaucomaModel(e.target.value)}
              placeholder="e.g., google/vit-base-patch16-224"
              className="w-full px-4 py-2 border rounded-lg"
            />
            <p className="text-sm text-gray-500 mt-2">Enter HuggingFace model ID</p>
          </div>
          <button
            onClick={switchGlaucomaModel}
            disabled={loading || !newGlaucomaModel}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Switching...' : 'Switch Model'}
          </button>
        </div>

        <div className="p-6 bg-white rounded-lg shadow">
          <h3 className="text-lg font-bold mb-4">Switch LLM Model</h3>
          <div className="mb-4">
            <input
              type="text"
              value={newLLMModel}
              onChange={(e) => setNewLLMModel(e.target.value)}
              placeholder="e.g., mistralai/Mistral-7B"
              className="w-full px-4 py-2 border rounded-lg"
            />
            <p className="text-sm text-gray-500 mt-2">Enter HuggingFace model ID</p>
          </div>
          <button
            onClick={switchLLMModel}
            disabled={loading || !newLLMModel}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Switching...' : 'Switch Model'}
          </button>
        </div>
      </div>

      {/* Quick Links */}
      <div className="mt-8">
        <button
          onClick={() => navigate('/diagnosis')}
          className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
        >
          New Diagnosis
        </button>
      </div>
    </div>
  );
}
