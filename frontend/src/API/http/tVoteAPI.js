import axios from "axios";

export const API_URL = `${process.env.REACT_APP_API_HOST}`;

const $api = axios.create({
    baseURL: API_URL,
    withCredentials: true
})

$api.interceptors.request.use((config) => {
    const access_token = localStorage.getItem('access_token')
    if (access_token) {
        config.headers.Authorization = `Bearer ${access_token}`;
    }

    return config;
})


export default $api;