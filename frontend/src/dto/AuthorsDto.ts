export interface GetAuthorsParams {
  name?: string;
  limit?: number;
  offset?: number;
}

export interface AuthorResponseDto {
  id: number;
  name: string;
}

export interface GetAuthorsResponseDto {
  authors: AuthorResponseDto[];
  total_results: number;
}

export interface PostBodyCreateAuthorDto {
  name: string;
}

export interface DeleteAuthorsBatchDto {
  ids: number[]
}
