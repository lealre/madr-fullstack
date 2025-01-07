import useRootApiService from "@/api/rootApi";
import {ApiResponseDto} from "@/dto/ApiResponseDto";
import {
  GetCurrentUserDto,
  SingUpRequestDto,
  SingUpResponseDto,
} from "@/dto/UsersDto";

const useUsersService = () => {
  const { PostWithoutRefreshToken, Get } = useRootApiService();

  const createUser = async (
    SingUpRequestDto: SingUpRequestDto
  ): Promise<ApiResponseDto<SingUpResponseDto>> => {
    const response = await PostWithoutRefreshToken<
      SingUpResponseDto,
      SingUpRequestDto
    >("/users/singup", SingUpRequestDto);

    return response;
  };

  const getCurrentUser = async (): Promise<
    ApiResponseDto<GetCurrentUserDto>
  > => {
    const response = await Get<GetCurrentUserDto>("/users/me");

    return response;
  };

  return { createUser, getCurrentUser };
};

export default useUsersService;
