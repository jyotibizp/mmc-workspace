import apiClient from '../api/client';

export const companiesService = {
  // Get all companies
  getCompanies: async (params = {}) => {
    const response = await apiClient.get('/companies', { params });
    return response.data;
  },

  // Get single company
  getCompany: async (companyId) => {
    const response = await apiClient.get(`/companies/${companyId}`);
    return response.data;
  },

  // Create company
  createCompany: async (companyData) => {
    const response = await apiClient.post('/companies', companyData);
    return response.data;
  },

  // Update company
  updateCompany: async (companyId, companyData) => {
    const response = await apiClient.put(`/companies/${companyId}`, companyData);
    return response.data;
  },

  // Delete company
  deleteCompany: async (companyId) => {
    const response = await apiClient.delete(`/companies/${companyId}`);
    return response.data;
  },

  // Search companies
  searchCompanies: async (query) => {
    const response = await apiClient.get('/companies/search', {
      params: { q: query }
    });
    return response.data;
  },

  // Get company statistics
  getCompaniesStats: async () => {
    const response = await apiClient.get('/companies/statistics');
    return response.data;
  }
};