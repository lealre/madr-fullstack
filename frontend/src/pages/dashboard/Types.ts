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
  searchQuery: string;
  setSearchQuery: (value: string) => void
  fetchAuthors: () => void;
}

export interface BooksTableProps {
  books: BookResponseDto[];
}
