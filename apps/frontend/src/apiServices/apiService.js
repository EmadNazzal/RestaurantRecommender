import axios from "axios";
import dayjs from "dayjs";

const API_BASE_URL = "https://nibble.rest/";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerUser = (data) => api.post("/api/register/", data);
export const loginUser = (data) => api.post("/api/login/", data);
export const resetPassword = (data) => api.post("/api/reset-password/", data);
export const refreshToken = (data) => api.post("/api/token/refresh/", data);
export const contactUs = (data) => api.post("/api/contact-us/", data);
export const getAllRestaurants = () => api.get("/api/all-restaurants/"); // DOES NOT WORK FOR NOW.
export const dropdownSearch = (query) =>
  api.get("/api/dropdown-search/", { params: { q: query } });
export const restuarantFreeTextEntry = (query) =>
  api.get("/api/free-text-restaurant-search/", { params: { query } });

export const getZoneForCurrentTime = () => {
  const currentTime = dayjs().format("YYYY-MM-DDTHH:mm:ss");
  return api.get(`/api/${currentTime}/zone/`);
};
