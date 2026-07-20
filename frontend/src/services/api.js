import axios from 'axios';

const API = axios.create({
  baseURL: 'https://phishguard-backend-53n8.onrender.com',
});

export default API;