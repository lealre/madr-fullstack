export interface getBooksParams {
  name?: string;
  year?: number;
  limit?: number;
  offset?: number;
}

export interface BookResponseDto {
  id: number;
  title: string
  year: number
  author_id: number;
}

export interface GetBooksResponseDto {
  books: BookResponseDto[];
//   total_results: number;
}
