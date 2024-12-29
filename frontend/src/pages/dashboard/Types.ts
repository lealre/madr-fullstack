import { AuthorResponseDto } from "@/dto/AuthorsDto";
import { BookResponseDto } from "@/dto/BooksDto";

export interface PageProps {
  totalResults: number;
  pageSize: number;
  currentPage: number;
  setCurrentPage: (newPage: number) => void;
}

export interface TabProps {
  value: string;
}

export interface AuthorsTableProps {
  authors: AuthorResponseDto[];
  page: number;
  fetchAuthors: (page: number) => void;
}

export interface BooksTableProps {
  books: BookResponseDto[];
}
