import axios from "axios";

const API_ENDPOINT = "/api/database";

const apiClient = axios.create({
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

// Add a request interceptor (optional)
apiClient.interceptors.request.use(
  (config) => {
    // You can add token headers or other modifications here before the request is sent
    // config.headers.Authorization = `Bearer ${yourToken}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor (optional)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with a status other than 2xx
      console.error("API Error:", error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error("Network Error:", error.request);
    } else {
      // Something else happened while setting up the request
      console.error("Error:", error.message);
    }
    return Promise.reject(error);
  }
);

export const connService = {
  initialize: () => {
    if (typeof window !== "undefined") {
      // Set the baseURL dynamically on the client-side
      apiClient.defaults.baseURL = window.location.origin;
    }
  },
  get: (params = {}, options = {}) => {
    return apiClient.get(API_ENDPOINT, { params, ...options });
  },
  post: (data, options = {}) => {
    return apiClient.post(API_ENDPOINT, data, options);
  },
  delete: (options = {}) => {
    return apiClient.delete(API_ENDPOINT, options);
  },
};
