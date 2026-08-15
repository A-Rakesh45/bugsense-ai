import api from './api';

export const bugService = {
  getBugs: async (params = {}) => {
    const res = await api.get('/bugs', { params });
    return res.data;
  },

  getBugById: async (id) => {
    const res = await api.get(`/bugs/${id}`);
    return res.data;
  },

  createBug: async (bugData) => {
    const res = await api.post('/bugs', bugData);
    return res.data;
  },

  updateBug: async (id, bugData) => {
    const res = await api.put(`/bugs/${id}`, bugData);
    return res.data;
  },

  deleteBug: async (id) => {
    const res = await api.delete(`/bugs/${id}`);
    return res.data;
  },

  retriggerPrediction: async (id) => {
    const res = await api.post(`/bugs/${id}/predict`);
    return res.data;
  },

  getSimilarBugs: async (id) => {
    const res = await api.get(`/bugs/${id}/similar`);
    return res.data;
  }
};
