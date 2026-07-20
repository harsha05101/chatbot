import axios from 'axios';

// Create and export a configured Axios instance
const API = axios.create({
  baseURL: 'http://localhost:5000',
});

export default API;