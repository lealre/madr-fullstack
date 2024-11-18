import { Button, Flex, Input, Stack, Table } from "@chakra-ui/react";
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

interface AuthorFormProps {
  name: string;
}

const AuthorsTable: React.FC<
  AuthorsTableProps & { fetchAuthors: () => void }
> = ({ authors, fetchAuthors }) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AuthorFormProps>();
  const [error, setError] = useState<string>();

  const handleAddAuthor = handleSubmit(async (data) => {
    const token = localStorage.getItem("token");
    try {
      await api.post("/author/", data, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      fetchAuthors(); // Refresh the authors list
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

      {/* Table */}
      <Table.Root key="outline" size="md" variant="outline" borderRadius="8px">
        <Table.Header bg="teal.500">
          <Table.Row>
            <Table.ColumnHeader>ID</Table.ColumnHeader>
            <Table.ColumnHeader textAlign="end">Author</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {authors.length > 0 ? (
            authors.map((item) => (
              <Table.Row key={item.id}>
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
      {error && <AlertMessage type="error" message={error} />}
    </>
  );
};

export default AuthorsTable;
