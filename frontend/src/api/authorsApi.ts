import useRootApiService from "@/api/rootApi";
import ApiResponseDto from "@/dto/ApiResponseDto";
import {
  GetAuthorsResponseDto,
  GetAuthorsParams,
  AuthorResponseDto,
  PostBodyCreateAuthorDto,
} from "@/dto/AuthorsDto";

const useAuthorsService = () => {
  const { Get, Post } = useRootApiService();

  const getAuthors = async (
    params?: GetAuthorsParams
  ): Promise<ApiResponseDto<GetAuthorsResponseDto>> => {
    const response = await Get<GetAuthorsResponseDto>("/author/", params);

    return response;
  };

  const createAuthor = async (
    data: PostBodyCreateAuthorDto
  ): Promise<ApiResponseDto<AuthorResponseDto>> => {
    const response = await Post<AuthorResponseDto, PostBodyCreateAuthorDto>(
      "/author/",
      data
    );

    return response;
  };

  return { getAuthors, createAuthor };
};

export default useAuthorsService;
