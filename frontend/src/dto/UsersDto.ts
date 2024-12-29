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

export interface GetCurrentUserDto {
  id: number;
  username: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
  is_superuser: boolean;
  is_active: boolean;
  is_verified: boolean;
}
