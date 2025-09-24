import apiClient from '../api/client';

export const campaignsService = {
  // Get all campaigns
  getCampaigns: async (params = {}) => {
    const response = await apiClient.get('/campaigns', { params });
    return response.data;
  },

  // Get single campaign
  getCampaign: async (campaignId) => {
    const response = await apiClient.get(`/campaigns/${campaignId}`);
    return response.data;
  },

  // Create campaign
  createCampaign: async (campaignData) => {
    const response = await apiClient.post('/campaigns', campaignData);
    return response.data;
  },

  // Update campaign
  updateCampaign: async (campaignId, campaignData) => {
    const response = await apiClient.put(`/campaigns/${campaignId}`, campaignData);
    return response.data;
  },

  // Delete campaign
  deleteCampaign: async (campaignId) => {
    const response = await apiClient.delete(`/campaigns/${campaignId}`);
    return response.data;
  },

  // Archive campaign
  archiveCampaign: async (campaignId) => {
    const response = await apiClient.post(`/campaigns/${campaignId}/archive`);
    return response.data;
  },

  // Get campaign statistics
  getCampaignsStats: async () => {
    const response = await apiClient.get('/campaigns/statistics');
    return response.data;
  },

  // Campaign Notes
  // Create campaign note
  createNote: async (noteData) => {
    const response = await apiClient.post('/campaigns/notes', noteData);
    return response.data;
  },

  // Get campaign notes
  getCampaignNotes: async (campaignId) => {
    const response = await apiClient.get(`/campaigns/${campaignId}/notes`);
    return response.data;
  },

  // Get single note
  getNote: async (noteId) => {
    const response = await apiClient.get(`/campaigns/notes/${noteId}`);
    return response.data;
  },

  // Update note
  updateNote: async (noteId, noteData) => {
    const response = await apiClient.put(`/campaigns/notes/${noteId}`, noteData);
    return response.data;
  },

  // Delete note
  deleteNote: async (noteId) => {
    const response = await apiClient.delete(`/campaigns/notes/${noteId}`);
    return response.data;
  },

  // Get overdue follow-ups
  getOverdueFollowUps: async () => {
    const response = await apiClient.get('/campaigns/follow-ups/overdue');
    return response.data;
  },

  // Get notes by opportunity
  getNotesByOpportunity: async (opportunityId) => {
    const response = await apiClient.get(`/campaigns/notes/by-opportunity/${opportunityId}`);
    return response.data;
  }
};