import apiClient from '../api/client';

export const opportunitiesService = {
  // Get all opportunities
  getOpportunities: async (params = {}) => {
    const response = await apiClient.get('/opportunities', { params });
    return response.data;
  },

  // Get single opportunity
  getOpportunity: async (opportunityId) => {
    const response = await apiClient.get(`/opportunities/${opportunityId}`);
    return response.data;
  },

  // Create opportunity
  createOpportunity: async (opportunityData) => {
    const response = await apiClient.post('/opportunities', opportunityData);
    return response.data;
  },

  // Update opportunity
  updateOpportunity: async (opportunityId, opportunityData) => {
    const response = await apiClient.put(`/opportunities/${opportunityId}`, opportunityData);
    return response.data;
  },

  // Delete opportunity
  deleteOpportunity: async (opportunityId) => {
    const response = await apiClient.delete(`/opportunities/${opportunityId}`);
    return response.data;
  },

  // Get opportunities statistics
  getOpportunitiesStats: async () => {
    const response = await apiClient.get('/opportunities/statistics');
    return response.data;
  },

  // Update opportunity status
  updateStatus: async (opportunityId, status) => {
    const response = await apiClient.patch(`/opportunities/${opportunityId}/status`, { status });
    return response.data;
  }
};