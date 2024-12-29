export interface SingUpRequestDto {
  username: string;
  email: string;
  password: string;
}

export interface SingUpResponseDto {
  id: number;
  username: string;
  email: string;
}

export interface SignInDto {
  email: string;
  password: string;
}
