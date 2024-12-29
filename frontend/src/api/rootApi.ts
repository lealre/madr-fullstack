import { ApiResponseDto } from "@/dto/ApiResponseDto";
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
        }
        if (error.response.status === 500) {
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
        if (error.response.status === 401) {
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: error.response.data,
          };
          // navigate to home here
        }
        if (error.response.status == 422) {
          const formattedErrors = error.response.data.detail.map((err: any) => {
            return `Field ${err.loc[1]} invalid. ${err.msg}`;
          });
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: formattedErrors,
          };
        }
        return Promise.reject(error);
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
  );

  async function Get<T>(path: string, params?: any) {
    try {
      const response: AxiosResponse<T> | ApiResponseDto<T> =
        await axiosInstance.get(path, {
          params,
          paramsSerializer: (params) => {
            return qs.stringify(params, { arrayFormat: "repeat" });
          },
        });

      if ("status" in response && [200, 201].includes(response.status)) {
        return {
          data: response.data,
          success: true,
          code: response.status,
          error: undefined,
        };
      }

      return response as ApiResponseDto<T>;
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
      const response: AxiosResponse<T> | ApiResponseDto<T> =
        await axiosInstance.post(path, body, {
          headers: { Authorization: authorization },
        });
      if ("status" in response && [200, 201].includes(response.status)) {
        return {
          data: response.data,
          success: true,
          code: response.status,
          error: undefined,
        };
      }

      return response as ApiResponseDto<T>;
    } catch (error: any) {
      return {
        data: undefined,
        success: false,
        code: error.response.status,
        error: error.response.data,
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
        }
        if (error.response.status === 500) {
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
        if (error.response.status == 422) {
          const formattedErrors = error.response.data.detail.map((err: any) => {
            return `Field ${err.loc[1]} invalid. ${err.msg}`;
          });
          return {
            data: undefined,
            success: false,
            code: error.response.status,
            error: formattedErrors,
          };
        }
        return {
          data: undefined,
          success: false,
          code: error.response.status,
          error: error.response.data,
        };
      }
      return {
        data: undefined,
        success: false,
        code: null,
        error: {
          detail: "An unexpected error occurred.",
        },
      };
    }
  }

  async function Put<T, TBody>(
    path: string,
    body: TBody
  ): Promise<ApiResponseDto<T>> {
    try {
      const response: AxiosResponse<T> | ApiResponseDto<T> =
        await axiosInstance.put(path, body);
      if ("status" in response && [200, 201].includes(response.status)) {
        return {
          data: response.data,
          success: true,
          code: response.status,
          error: undefined,
        };
      }

      return response as ApiResponseDto<T>;
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
      const response: AxiosResponse<T> | ApiResponseDto<T> =
        await axiosInstance.patch(path, body);
      if ("status" in response && [200, 201].includes(response.status)) {
        return {
          data: response.data,
          success: true,
          code: response.status,
          error: undefined,
        };
      }

      return response as ApiResponseDto<T>;
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
      const response: AxiosResponse<T> | ApiResponseDto<T> =
        await axiosInstance.delete(path, {
          data: body,
        });
      if ("status" in response && [200, 201].includes(response.status)) {
        return {
          data: response.data,
          success: true,
          code: response.status,
          error: undefined,
        };
      }

      return response as ApiResponseDto<T>;
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
