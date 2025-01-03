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
    .string()
    .nonempty({ message: "Year is required" })
    .transform((val) => val.trim())
    .refine((val) => /^\d+$/.test(val), {
      message:
        "Year must be a valid number without any letters or special characters",
    })
    .transform((val) => {
      const num = parseInt(val, 10);
      return String(num);
    })
    .refine(
      (val) => {
        const numVal = parseInt(val, 10);
        return numVal >= 1 && numVal <= new Date().getFullYear();
      },
      {
        message: "Enter a valid year",
      }
    ),

  authorList: z
    .array(z.string({ invalid_type_error: "Author must be a string" }))
    .length(1, { message: "Author is required" }),
});

export type BookFormSchema = z.infer<typeof bookFormSchema>;

export interface AlertProps {
  open: boolean;
  setOpen: (value: boolean) => void;
  deleteFunction: () => void;
}
