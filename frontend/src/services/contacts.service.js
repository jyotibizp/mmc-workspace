import apiClient from '../api/client';

export const contactsService = {
  // Get all contacts
  getContacts: async (params = {}) => {
    const response = await apiClient.get('/contacts', { params });
    return response.data;
  },

  // Get single contact
  getContact: async (contactId) => {
    const response = await apiClient.get(`/contacts/${contactId}`);
    return response.data;
  },

  // Create contact
  createContact: async (contactData) => {
    const response = await apiClient.post('/contacts', contactData);
    return response.data;
  },

  // Update contact
  updateContact: async (contactId, contactData) => {
    const response = await apiClient.put(`/contacts/${contactId}`, contactData);
    return response.data;
  },

  // Delete contact
  deleteContact: async (contactId) => {
    const response = await apiClient.delete(`/contacts/${contactId}`);
    return response.data;
  },

  // Search contacts
  searchContacts: async (query) => {
    const response = await apiClient.get('/contacts/search', {
      params: { q: query }
    });
    return response.data;
  },

  // Get contacts by company
  getContactsByCompany: async (companyId) => {
    const response = await apiClient.get(`/contacts/by-company/${companyId}`);
    return response.data;
  },

  // Get contacts statistics
  getContactsStats: async () => {
    const response = await apiClient.get('/contacts/statistics');
    return response.data;
  }
};