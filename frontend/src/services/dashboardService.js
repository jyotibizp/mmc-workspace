import apiClient from '../api/client';

const dashboardService = {
  // Get comprehensive dashboard statistics
  getStatistics: async (dateRange = '30d') => {
    const response = await apiClient.get(`/dashboard/statistics?date_range=${dateRange}`);
    return response.data;
  },

  // Get opportunities analytics with trends
  getOpportunitiesAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get(`/dashboard/analytics/opportunities?date_range=${dateRange}`);
    return response.data;
  },

  // Get proposals analytics with conversion rates
  getProposalsAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get(`/dashboard/analytics/proposals?date_range=${dateRange}`);
    return response.data;
  },

  // Get campaigns analytics with performance metrics
  getCampaignsAnalytics: async (dateRange = '30d') => {
    const response = await apiClient.get(`/dashboard/analytics/campaigns?date_range=${dateRange}`);
    return response.data;
  },

  // Get recent activity timeline
  getRecentActivity: async (limit = 10) => {
    const response = await apiClient.get(`/dashboard/recent-activity?limit=${limit}`);
    return response.data;
  },

  // Get complete dashboard overview with all metrics
  getOverview: async () => {
    const response = await apiClient.get('/dashboard/overview');
    return response.data;
  }
};

export default dashboardService;