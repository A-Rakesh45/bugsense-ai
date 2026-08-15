import api from './api';

export const dashboardService = {
  getStatistics: async () => {
    const res = await api.get('/dashboard/statistics');
    return res.data;
  },

  submitFeedback: async (feedbackData) => {
    const res = await api.post('/feedback', feedbackData);
    return res.data;
  },

  getFeedbackLogs: async () => {
    const res = await api.get('/feedback');
    return res.data;
  }
};
