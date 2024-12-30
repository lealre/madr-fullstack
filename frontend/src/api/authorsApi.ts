import useRootApiService from "@/api/rootApi";
import { ApiResponseDto, MessageDto } from "@/dto/ApiResponseDto";
import {
  GetAuthorsResponseDto,
  GetAuthorsParams,
  AuthorResponseDto,
  PostBodyCreateAuthorDto,
  DeleteAuthorsBatchDto,
} from "@/dto/AuthorsDto";

const useAuthorsService = () => {
  const { Get, Post } = useRootApiService();

  const getAuthors = async (
    params?: GetAuthorsParams
  ): Promise<ApiResponseDto<GetAuthorsResponseDto>> => {
    const response = await Get<GetAuthorsResponseDto>("/author", params);

    return response;
  };

  const createAuthor = async (
    data: PostBodyCreateAuthorDto
  ): Promise<ApiResponseDto<AuthorResponseDto>> => {
    const response = await Post<AuthorResponseDto, PostBodyCreateAuthorDto>(
      "/author",
      data
    );

    return response;
  };

  const deleteAuthorsBatch = async (
    data: DeleteAuthorsBatchDto
  ): Promise<ApiResponseDto<MessageDto>> => {
    const response = await Post<MessageDto, DeleteAuthorsBatchDto>(
      "/author/delete/batch",
      data
    );

    return response;
  };

  return { getAuthors, createAuthor, deleteAuthorsBatch };
};

export default useAuthorsService;
