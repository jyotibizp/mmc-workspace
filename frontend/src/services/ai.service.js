import apiClient from '../api/client';

export const aiService = {
  // Analyze and extract post data
  analyzeExtractPost: async (postId) => {
    const response = await apiClient.post('/ai/analyze-extract', { post_id: postId });
    return response.data;
  },

  // Analyze opportunity (unified endpoint)
  analyzeOpportunity: async (postId, enableCache = true) => {
    const response = await apiClient.post('/ai/analyze-opportunity', {
      post_id: postId,
      enable_cache: enableCache
    });
    return response.data;
  },

  // Streaming AI analysis
  analyzeOpportunityStream: async (postId, enableCache = true) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/ai/analyze-opportunity/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Note: We'll need to handle auth token manually for streaming
      },
      body: JSON.stringify({
        post_id: postId,
        enable_cache: enableCache
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.body.getReader();
  },

  // Generate proposal with AI
  generateProposal: async (opportunityId, templateId = null, additionalContext = null) => {
    const response = await apiClient.post('/ai/generate-proposal', {
      opportunity_id: opportunityId,
      template_id: templateId,
      additional_context: additionalContext
    });
    return response.data;
  }
};