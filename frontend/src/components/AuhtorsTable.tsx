import {
  Button,
  Center,
  Flex,
  HStack,
  Input,
  Stack,
  Table,
} from "@chakra-ui/react";
import { InputGroup } from "./ui/input-group";
import { LuSearch } from "react-icons/lu";
import { GrAdd } from "react-icons/gr";
import React, { useState } from "react";
import { Field } from "@/components/ui/field";
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
import {
  ActionBarContent,
  ActionBarRoot,
  ActionBarSelectionTrigger,
  ActionBarSeparator,
} from "@/components/ui/action-bar";
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination";
import { Checkbox } from "@/components/ui/checkbox";
import { useForm } from "react-hook-form";
import api from "../api";
import axios from "axios";
import AlertMessage from "../components/AlertMessage";

interface AuthorsProps {
  id: number;
  name: string;
}

export interface AuthorsTableProps {
  authors: AuthorsProps[];
}

export interface PageProps {
  totalPages: number;
  pageSize: number;
  currentPage: number;
  setCurrentPage: (newPage: number) => void;
}

export interface ExtendedAuthorsTableProps extends AuthorsTableProps {
  fetchAuthors: (page: number) => void;
  pageProps: PageProps
}


interface AuthorFormProps {
  name: string;
}

const AuthorsTable: React.FC<ExtendedAuthorsTableProps> = ({
  authors,
  fetchAuthors,
  pageProps
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AuthorFormProps>();
  const [error, setError] = useState<string>();

  const { totalPages, pageSize, currentPage, setCurrentPage } = pageProps;

  const [selection, setSelection] = useState<number[]>([]);
  const hasSelection = selection.length > 0;
  const indeterminate = hasSelection && selection.length < authors.length;

  console.log("Total pages: ", totalPages);
  console.log("paze size: ", pageSize);
  const handleAddAuthor = handleSubmit(async (data) => {
    const token = localStorage.getItem("token");
    try {
      await api.post("/author/", data, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      fetchAuthors(currentPage);
      reset();
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          console.error("No response from the server:", err);
          setError("Unable to reach the server. Please try again later.");
        } else if (err.response.status === 500) {
          console.error("Server error:", err.response);
          setError(
            "An internal server error occurred. Please try again later."
          );
        } else if (err.response.status === 401) {
          console.error("Authentication error:", err.response);
          setError("Invalid login credentials.");
        } else if (err.response.status === 400) {
          console.error("Author already registered:", err.response);
          setError("Author already registered");
        } else {
          console.error("Error:", err.response);
          setError("An unexpected error occurred. Please try again.");
        }
      } else {
        console.error("Non-Axios error:", err);
        setError("An unexpected error occurred.");
      }
    }
  });

  return (
    <>
      <Flex gap="4" justify="space-between" mb={2}>
        <InputGroup flex="1" startElement={<LuSearch />}>
          <Input maxW="400px" placeholder="Search authors" />
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
          <DialogContent colorPalette="teal" bg="teal.50">
            <DialogHeader>
              <DialogTitle>New Author</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleAddAuthor}>
              <DialogBody pb="4">
                <Stack gap="4">
                  <Field
                    label="Author Name"
                    invalid={!!errors.name}
                    errorText={errors.name?.message}
                  >
                    <Input
                      {...register("name", {
                        required: "Name is required",
                        maxLength: {
                          value: 50, // Maximum number of characters allowed
                          message: "Name cannot exceed 50 characters", // Custom error message
                        },
                      })}
                    />
                  </Field>
                </Stack>
              </DialogBody>
              <DialogFooter>
                <Button>Cancel</Button>
                <Button type="submit">Add</Button>
              </DialogFooter>
            </form>
            <DialogCloseTrigger />
          </DialogContent>
        </DialogRoot>
      </Flex>

      <Flex direction="column" gap={3}>
        <Table.Root
          key="outline"
          // size="md"
          variant="outline"
          borderRadius="8px"
        >
          <Table.Header bg="teal.500">
            <Table.Row>
              <Table.ColumnHeader>
                <Checkbox
                  top="1"
                  _hover={{ cursor: "pointer" }}
                  aria-label="Select all rows"
                  checked={
                    indeterminate ? "indeterminate" : selection.length > 0
                  }
                  onCheckedChange={(changes) => {
                    setSelection(
                      changes.checked ? authors.map((item) => item.id) : []
                    );
                  }}
                />
              </Table.ColumnHeader>
              <Table.ColumnHeader>ID</Table.ColumnHeader>
              <Table.ColumnHeader textAlign="end">Author</Table.ColumnHeader>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {authors.length > 0 ? (
              authors.map((item) => (
                <Table.Row
                  key={item.id}
                  data-selected={selection.includes(item.id) ? "" : undefined}
                  bg={selection.includes(item.id) ? "teal.100" : "white"}
                >
                  <Table.Cell>
                    <Checkbox
                      variant="solid"
                      colorPalette="teal"
                      top="1"
                      _hover={{ cursor: "pointer" }}
                      aria-label="Select row"
                      checked={selection.includes(item.id)}
                      onCheckedChange={(changes) => {
                        setSelection((prev) =>
                          changes.checked
                            ? [...prev, item.id]
                            : selection.filter((id) => id !== item.id)
                        );
                      }}
                    />
                  </Table.Cell>
                  <Table.Cell>{item.id}</Table.Cell>
                  <Table.Cell textAlign="end">{item.name}</Table.Cell>
                </Table.Row>
              ))
            ) : (
              <Table.Row>
                <Table.Cell colSpan={2} textAlign="center">
                  No authors available
                </Table.Cell>
              </Table.Row>
            )}
          </Table.Body>
        </Table.Root>

        <Center>
          <PaginationRoot
            count={totalPages}
            pageSize={pageSize}
            defaultPage={1}
            page={currentPage}
            onPageChange={(e) => {
              console.log(e.page);
              setCurrentPage(e.page);
            }}
            size="sm"
            color="teal.600"
          >
            <HStack>
              <PaginationPrevTrigger color="black" />
              <PaginationItems color="black" />
              <PaginationNextTrigger color="black" />
            </HStack>
          </PaginationRoot>
        </Center>
      </Flex>
      <ActionBarRoot open={hasSelection}>
        <ActionBarContent bg="teal.50" borderWidth="1px">
          <ActionBarSelectionTrigger>
            {selection.length} selected
          </ActionBarSelectionTrigger>
          <ActionBarSeparator />
          <Button
            size="sm"
            colorPalette="red"
            _hover={{ background: "red.400" }}
          >
            Delete
          </Button>
        </ActionBarContent>
      </ActionBarRoot>

      {error && <AlertMessage type="error" message={error} />}
    </>
  );
};

export default AuthorsTable;
