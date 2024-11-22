import axios, { AxiosInstance, InternalAxiosRequestConfig } from "axios";

const baseURL = "http://localhost:8000";

const useRootApiService = () => {
  const axiosInstance: AxiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 20000,
  });

  axiosInstance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const authToken = localStorage.getItem("token");

      if (authToken) {
        config.headers["Authorization"] = `Bearer ${authToken}`;
      }

      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  return axiosInstance

};

export default useRootApiService;
