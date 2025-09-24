import apiClient from '../api/client';

export const proposalsService = {
  // Get all proposals
  getProposals: async (params = {}) => {
    const response = await apiClient.get('/proposals', { params });
    return response.data;
  },

  // Get single proposal
  getProposal: async (proposalId) => {
    const response = await apiClient.get(`/proposals/${proposalId}`);
    return response.data;
  },

  // Create proposal
  createProposal: async (proposalData) => {
    const response = await apiClient.post('/proposals', proposalData);
    return response.data;
  },

  // Update proposal
  updateProposal: async (proposalId, proposalData) => {
    const response = await apiClient.put(`/proposals/${proposalId}`, proposalData);
    return response.data;
  },

  // Delete proposal
  deleteProposal: async (proposalId) => {
    const response = await apiClient.delete(`/proposals/${proposalId}`);
    return response.data;
  },

  // Generate AI proposal
  generateAIProposal: async (opportunityId, additionalContext) => {
    const response = await apiClient.post('/proposals/generate-ai', null, {
      params: { opportunity_id: opportunityId, additional_context: additionalContext }
    });
    return response.data;
  },

  // Export proposal
  exportProposal: async (proposalId, format = 'markdown') => {
    const response = await apiClient.get(`/proposals/${proposalId}/export`, {
      params: { format },
      responseType: 'blob' // For file download
    });
    return response.data;
  },

  // Duplicate proposal
  duplicateProposal: async (proposalId, newOpportunityId) => {
    const response = await apiClient.post(`/proposals/${proposalId}/duplicate`, null, {
      params: { new_opportunity_id: newOpportunityId }
    });
    return response.data;
  },

  // Get proposal by opportunity
  getProposalByOpportunity: async (opportunityId) => {
    const response = await apiClient.get(`/proposals/by-opportunity/${opportunityId}`);
    return response.data;
  },

  // Get proposals statistics
  getProposalsStats: async () => {
    const response = await apiClient.get('/proposals/statistics');
    return response.data;
  }
};