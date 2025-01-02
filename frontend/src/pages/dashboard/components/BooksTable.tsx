import React, { useState } from "react";
import { GrAdd } from "react-icons/gr";
import { LuSearch } from "react-icons/lu";
import {
  Button,
  createListCollection,
  Flex,
  Input,
  ListCollection,
  Stack,
  Table,
} from "@chakra-ui/react";
import { Checkbox } from "@/components/ui/checkbox";
import { InputGroup } from "@/components/ui/input-group";

import {
  bookFormSchema,
  BookFormSchema,
  BooksTableProps,
} from "@/pages/dashboard/Types";
import {
  ActionBarContent,
  ActionBarRoot,
  ActionBarSelectionTrigger,
  ActionBarSeparator,
} from "@/components/ui/action-bar";
import { toaster } from "@/components/ui/toaster";
import useBooksService from "@/api/booksApi";
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Field } from "@/components/ui/field";
import { Controller, useForm } from "react-hook-form";
import { PostBodyCreateBookDto } from "@/dto/BooksDto";
import { AuthorResponseDto } from "@/dto/AuthorsDto";
import {
  SelectContent,
  SelectItem,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
} from "@/components/ui/select";
import { zodResolver } from "@hookform/resolvers/zod";

const BooksTable: React.FC<BooksTableProps> = ({
  books,
  authors,
  searchQuery,
  setCurrentPage,
  currentPage,
  setSearchQuery,
  fetchBooks,
}) => {
  const { createBook, deleteBooksBatch } = useBooksService();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
    control,
  } = useForm<BookFormSchema>({
    mode: "onChange",
    resolver: zodResolver(bookFormSchema),
  });

  const [booksIDs, setBooksIDs] = useState<number[]>([]);
  const hasSelection = booksIDs.length > 0;
  const indeterminate = hasSelection && booksIDs.length < books.length;

  const transformAuthorsToListCollection = (authors: AuthorResponseDto[]) => {
    return createListCollection({
      items: authors.map((author) => ({
        label: author.name,
        value: String(author.id),
      })),
    });
  };

  const authorList: ListCollection<{
    label: string;
    value: string;
  }> = transformAuthorsToListCollection(authors);

  const handleAddBook = handleSubmit(async (formData) => {
    const data: PostBodyCreateBookDto = {
      title: formData.title,
      year: formData.year,
      author_id: Number(formData.authorList),
    };

    const response = await createBook(data);
    if (response.data && response.success) {
      reset();
      toaster.create({
        title: "New book created.",
        type: "success",
      });
    } else {
      if (Array.isArray(response.error)) {
        response.error.forEach((errorMsg: string) => {
          toaster.create({
            title: errorMsg,
            type: "error",
          });
        });
      } else {
        toaster.create({
          title: response.error?.detail ?? "An error occurred",
          type: "error",
        });
      }
    }
  });

  const deleteBooks = async () => {
    const response = await deleteBooksBatch({ ids: booksIDs });
    if (response.data && response.success) {
      toaster.create({
        title: response.data.message,
        type: "success",
      });
      fetchBooks();
      setBooksIDs([]);
    } else {
      toaster.create({
        title: response.error?.detail ?? "An error occurred",
        type: "error",
      });
    }
  };

  const handleSearch = async () => {
    if (currentPage !== 1) {
      setCurrentPage(1);
    } else {
      fetchBooks();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <>
      <Flex gap="4" justify="space-between" mb={2}>
        <InputGroup flex="1" startElement={<LuSearch />}>
          <Input
            borderColor="border.emphasized"
            borderWidth={2}
            focusRing="inside"
            focusRingColor="teal.focusRing"
            maxW="400px"
            placeholder="Search by book name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </InputGroup>

        <DialogRoot
          key="center"
          placement="center"
          motionPreset="slide-in-bottom"
        >
          <DialogTrigger asChild>
            <Button
              height="10"
              width="30"
              background="teal.500"
              marginEnd="auto"
              borderRadius="md"
              _hover={{ background: "teal.600" }}
            >
              <GrAdd size={20} color="white" />
            </Button>
          </DialogTrigger>
          <DialogContent colorPalette="teal" bg="white">
            <DialogHeader>
              <DialogTitle>New Author</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleAddBook}>
              <DialogBody pb="4">
                <Stack gap="4">
                  <Field
                    label="Book title"
                    invalid={!!errors.title}
                    errorText={errors.title?.message}
                  >
                    <Input
                      {...register("title", {
                        required: "Name is required",
                        maxLength: {
                          value: 50,
                          message: "Name cannot exceed 50 characters",
                        },
                      })}
                    />
                  </Field>
                  <Field
                    label="Year"
                    invalid={!!errors.year}
                    errorText={errors.year?.message}
                  >
                    <Input
                      {...register("year", {
                        required: "Year is required",
                        maxLength: {
                          value: 4,
                          message: "Year cannot exceed 4 numbers",
                        },
                        setValueAs: (value) => parseInt(value, 10),
                      })}
                    />
                  </Field>
                  <Field
                    label="Rating"
                    invalid={!!errors.authorList}
                    errorText={errors.authorList?.message}
                    width="320px"
                  >
                    <Controller
                      control={control}
                      name="authorList"
                      render={({ field }) => (
                        <SelectRoot
                          name={field.name}
                          value={field.value}
                          onValueChange={({ value }) => {
                            field.onChange(value);
                          }}
                          onInteractOutside={() => field.onBlur()}
                          collection={authorList}
                        >
                          <SelectTrigger>
                            <SelectValueText placeholder="Select movie" />
                          </SelectTrigger>
                          <SelectContent zIndex="popover" bgColor="white">
                            {authorList.items.map((author) => (
                              <SelectItem
                                item={author}
                                key={author.value}
                                _hover={{
                                  bgColor: "teal.100",
                                  cursor: "pointer",
                                }}
                                _selected={{
                                  bgColor: "teal.100",
                                  cursor: "pointer",
                                }}
                              >
                                {author.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </SelectRoot>
                      )}
                    />
                  </Field>
                </Stack>
              </DialogBody>
              <DialogFooter>
                <Button onClick={() => reset()}>Cancel</Button>
                <Button type="submit">Add</Button>
              </DialogFooter>
            </form>
            <DialogCloseTrigger />
          </DialogContent>
        </DialogRoot>
      </Flex>

      <Table.Root size="sm" variant="line">
        <Table.Header bg="teal.500">
          <Table.Row borderBottomWidth={3} borderColor="border.emphasized">
            <Table.ColumnHeader width="10%">
              <Checkbox
                borderColor="black"
                borderWidth={1}
                top="1"
                _hover={{ cursor: "pointer" }}
                aria-label="Select all rows"
                checked={indeterminate ? "indeterminate" : booksIDs.length > 0}
                onCheckedChange={(changes) => {
                  setBooksIDs(
                    changes.checked ? books.map((item) => item.id) : []
                  );
                }}
              />
            </Table.ColumnHeader>
            <Table.ColumnHeader width="50%">Title</Table.ColumnHeader>
            <Table.ColumnHeader width="20%">Year</Table.ColumnHeader>
            <Table.ColumnHeader width="20%" textAlign="end">
              Author
            </Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {books.map((item) => (
            <Table.Row
              key={item.id}
              borderBottomWidth={2}
              borderColor="border.emphasized"
              data-selected={booksIDs.includes(item.id) ? "" : undefined}
              bg={booksIDs.includes(item.id) ? "teal.100" : "white"}
            >
              <Table.Cell>
                <Checkbox
                  borderColor="border.inverted"
                  borderWidth={1}
                  top="1"
                  variant="solid"
                  colorPalette="teal"
                  _hover={{ cursor: "pointer" }}
                  aria-label="Select row"
                  checked={booksIDs.includes(item.id)}
                  onCheckedChange={(changes) => {
                    setBooksIDs((prev) =>
                      changes.checked
                        ? [...prev, item.id]
                        : booksIDs.filter((id) => id !== item.id)
                    );
                  }}
                />
              </Table.Cell>
              <Table.Cell>{item.title}</Table.Cell>
              <Table.Cell>{item.year}</Table.Cell>
              <Table.Cell textAlign="end">{item.author}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>

      <ActionBarRoot open={hasSelection}>
        <ActionBarContent bg="teal.50" borderWidth="1px">
          <ActionBarSelectionTrigger>
            {booksIDs.length} selected
          </ActionBarSelectionTrigger>
          <ActionBarSeparator />
          <Button
            size="sm"
            colorPalette="red"
            _hover={{ background: "red.400" }}
            onClick={() => deleteBooks()}
          >
            Delete
          </Button>
          <Button
            size="sm"
            colorPalette="blue"
            _hover={{ background: "blue.400" }}
            onClick={() => setBooksIDs([])}
          >
            Clear Selection
          </Button>
        </ActionBarContent>
      </ActionBarRoot>
    </>
  );
};

export default BooksTable;
