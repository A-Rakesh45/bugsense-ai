import api from './api';

export const authService = {
  login: async (username, password) => {
    const res = await api.post('/auth/login', { username, password });
    if (res.data.access_token) {
      localStorage.setItem('bugsense_token', res.data.access_token);
      localStorage.setItem('bugsense_user', JSON.stringify(res.data.user));
    }
    return res.data;
  },

  register: async (userData) => {
    const res = await api.post('/auth/register', userData);
    return res.data;
  },

  getMe: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  },

  logout: () => {
    localStorage.removeItem('bugsense_token');
    localStorage.removeItem('bugsense_user');
  }
};
