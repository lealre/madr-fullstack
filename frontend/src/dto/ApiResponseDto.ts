export interface ApiResponseDto<T> {
  data: T | undefined;
  success: boolean;
  code: number | null;
  error: any;
}

export interface MessageDto {
  message: string;
}
