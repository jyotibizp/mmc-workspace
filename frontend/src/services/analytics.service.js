import apiClient from '../api/client';

export const analyticsService = {
  // Get dashboard statistics
  getDashboardStats: async () => {
    const response = await apiClient.get('/analytics/dashboard');
    return response.data;
  },

  // Get opportunities analytics
  getOpportunitiesAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get('/analytics/opportunities', {
      params: { date_range: dateRange }
    });
    return response.data;
  },

  // Get proposals analytics
  getProposalsAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get('/analytics/proposals', {
      params: { date_range: dateRange }
    });
    return response.data;
  },

  // Get campaigns analytics
  getCampaignsAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get('/analytics/campaigns', {
      params: { date_range: dateRange }
    });
    return response.data;
  },

  // Get revenue analytics
  getRevenueAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get('/analytics/revenue', {
      params: { date_range: dateRange }
    });
    return response.data;
  },

  // Get activity timeline
  getActivityTimeline: async (limit = 50) => {
    const response = await apiClient.get('/analytics/activity', {
      params: { limit }
    });
    return response.data;
  }
};