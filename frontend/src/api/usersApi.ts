import useRootApiService from "@/api/rootApi";
import ApiResponseDto from "@/dto/ApiResponseDto";
import { SingUpRequestDto, SingUpResponseDto } from "@/dto/UsersDto";

const useUsersService = () => {
  const { PostWithoutRefreshToken } = useRootApiService();

  const createUser = async (
    SingUpRequestDto: SingUpRequestDto
  ): Promise<ApiResponseDto<SingUpResponseDto>> => {
    const response = await PostWithoutRefreshToken<
      SingUpResponseDto,
      SingUpRequestDto
    >("/users/singup", SingUpRequestDto);

    return response;
  };

  return { createUser };
};

export default useUsersService;
