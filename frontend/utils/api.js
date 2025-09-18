// utils/api.js
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Always attach token (no skipping here)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ===== AUTH =====
export const signup = async (data) => {
  try {
    const res = await api.post("/auth/signup", data);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

export const login = async (data) => {
  try {
    const res = await api.post("/auth/login", data);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

// ===== EVENTS =====
// Public (no auth)
export const getEvents = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/events/`); // plain axios, no auth
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

// Protected (with auth)
export const getEvent = async (id) => {
  try {
    const res = await api.get(`/events/${id}`);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

export const createEvent = async (data) => {
  try {
    const res = await api.post("/events/", data);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

export const updateEvent = async (id, data) => {
  try {
    const res = await api.put(`/events/${id}`, data);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};

export const deleteEvent = async (id) => {
  try {
    const res = await api.delete(`/events/${id}`);
    return res.data;
  } catch (err) {
    throw err.response || err;
  }
};
