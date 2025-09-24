import apiClient from '../api/client';

export const linkedinService = {
  // Get LinkedIn posts
  getPosts: async (params = {}) => {
    const response = await apiClient.get('/linkedin/posts', { params });
    return response.data;
  },

  // Get single post
  getPost: async (postId) => {
    const response = await apiClient.get(`/linkedin/posts/${postId}`);
    return response.data;
  },

  // Ingest single post
  ingestPost: async (postData) => {
    const response = await apiClient.post('/linkedin/ingest', postData);
    return response.data;
  },

  // Batch ingest posts
  batchIngestPosts: async (postsData) => {
    const response = await apiClient.post('/linkedin/ingest/batch', { posts: postsData });
    return response.data;
  },

  // Delete post
  deletePost: async (postId) => {
    const response = await apiClient.delete(`/linkedin/posts/${postId}`);
    return response.data;
  },

  // Get posts statistics
  getPostsStats: async () => {
    const response = await apiClient.get('/linkedin/posts/statistics');
    return response.data;
  }
};