import ApiResponseDto from "@/dto/ApiResponseDto";
import axios, {
  AxiosInstance,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";
import qs from "qs";

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

  axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (axios.isAxiosError(error)) {
        if (!error.response) {
          return {
            data: undefined,
            success: false,
            code: null,
            error: {
              detail: "Unable to reach the server. Please try again later.",
            },
          };
        } else if (error.response.status === 500) {
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: {
              detail:
                "An internal server error occurred. Please try again later.",
            },
          };
        } else if (error.response.status === 401) {
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: error.response.data,
          };
          // navigate to home here
        }
      } else {
        return {
          data: undefined,
          success: false,
          code: null,
          error: {
            detail: "An unexpected error occurred. Please try again.",
          },
        };
      }
      return Promise.reject(error);
    }
  );

  async function Get<T>(path: string, params?: any) {
    try {
      const response: AxiosResponse<T> = await axiosInstance.get(path, {
        params,
        paramsSerializer: (params) => {
          return qs.stringify(params, { arrayFormat: "repeat" });
        },
      });
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response?.status,
        error: error.response?.data,
      };
    }
  }

  async function Post<T, TBody>(
    path: string,
    body: TBody,
    authorization?: string | undefined
  ): Promise<ApiResponseDto<T>> {
    try {
      const response: AxiosResponse<T> = await axiosInstance.post(path, body, {
        headers: { Authorization: authorization },
      });
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response?.status,
        error: error.response?.data,
      };
    }
  }

  async function PostWithoutRefreshToken<T, TBody>(
    path: string,
    body: TBody
  ): Promise<ApiResponseDto<T>> {
    const tempInstance: AxiosInstance = axios.create({
      baseURL: baseURL,
      timeout: 30000,
    });

    try {
      const response: AxiosResponse<T> = await tempInstance.post(path, body);
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error) {
      console.log(error);
      if (axios.isAxiosError(error)) {
        console.log(error);
        if (!error.response) {
          return {
            data: undefined,
            success: false,
            code: null,
            error: {
              detail: "Unable to reach the server. Please try again later.",
            },
          };
        } else if (error.response.status === 500) {
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: {
              detail:
                "An internal server error occurred. Please try again later.",
            },
          };
        }
      }
      return {
        data: undefined,
        success: false,
        code: null,
        error: {
          detail: "An unexpected error occurred. Please try again.",
        },
      };
    }
  }

  async function Put<T, TBody>(
    path: string,
    body: TBody
  ): Promise<ApiResponseDto<T>> {
    try {
      const response: AxiosResponse<T> = await axiosInstance.put(path, body);
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response.status,
        error: error.response.data,
      };
    }
  }

  async function Patch<T, TBody>(
    path: string,
    body: TBody
  ): Promise<ApiResponseDto<T>> {
    try {
      const response: AxiosResponse<T> = await axiosInstance.patch(path, body);
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response.status,
        error: error.response.data,
      };
    }
  }

  async function Delete<T, TBody>(
    path: string,
    body?: TBody
  ): Promise<ApiResponseDto<T>> {
    try {
      const response: AxiosResponse<T> = await axiosInstance.delete(path, {
        data: body,
      });
      return {
        data: response.data,
        success: true,
        code: response.status,
        error: undefined,
      };
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response.status,
        error: error.response.data,
      };
    }
  }

  return { Get, Post, PostWithoutRefreshToken, Put, Patch, Delete };
};

export default useRootApiService;
