import useRootApiService from "@/api/rootApi";
import ApiResponseDto from "@/dto/ApiResponseDto";
import { GetBooksResponseDto, getBooksParams } from "@/dto/BooksDto";

const useBooksService = () => {
  const { Get } = useRootApiService();

  const getBooks = async (
    params?: getBooksParams
  ): Promise<ApiResponseDto<GetBooksResponseDto>> => {
    const response = await Get<GetBooksResponseDto>("/book", params);

    return response;
  };

  return { getBooks };
};

export default useBooksService;
