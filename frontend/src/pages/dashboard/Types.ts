import { AuthorResponseDto } from "@/dto/AuthorsDto";
import { BookResponseDto } from "@/dto/BooksDto";

import { z } from "zod";

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
  setSearchQuery: (value: string) => void;
  currentPage: number;
  setCurrentPage: (value: number) => void;
  fetchAuthors: () => void;
}

export interface BooksTableProps {
  books: BookResponseDto[];
  authors: AuthorResponseDto[];
  searchQuery: string;
  setSearchQuery: (value: string) => void;
  setCurrentPage: (value: number) => void;
  currentPage: number;
  fetchBooks: () => void;
}

export const bookFormSchema = z.object({
  title: z.string().nonempty({ message: "Title is required" }),
  year: z
    .number({ invalid_type_error: "Year must be a number" })
    .min(1, { message: "Year must be a positive number" })
    .max(new Date().getFullYear(), { message: "Enter a valid year" }),
  authorList: z.string({ message: "Framework is required" }).array(),
});

export type BookFormSchema = z.infer<typeof bookFormSchema>;
