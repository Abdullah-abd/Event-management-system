// utils/api.js
import axios from "axios";

// Base URL for your API
const API_BASE_URL = "http://127.0.0.1:8000"; // replace with your actual API URL

// ===== AUTH =====
export const signup = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/signup`, data);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

export const login = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, data);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

// ===== EVENTS =====
export const getEvents = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/events/`);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

export const getEvent = async (eventId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/events/${eventId}`);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

export const createEvent = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/events/`, data);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

export const updateEvent = async (eventId, data) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/events/${eventId}`, data);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};

export const deleteEvent = async (eventId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/events/${eventId}`);
    return response.data;
  } catch (error) {
    throw error.response || error;
  }
};
