import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { LuSearch } from "react-icons/lu";
import { GrAdd } from "react-icons/gr";
import { Button, Flex, Input, Stack, Table } from "@chakra-ui/react";
import { InputGroup } from "@/components/ui/input-group";
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
import { toaster } from "@/components/ui/toaster";
import { Checkbox } from "@/components/ui/checkbox";

import useAuthorsService from "@/api/authorsApi";
import { PostBodyCreateAuthorDto } from "@/dto/AuthorsDto";
import { AuthorsTableProps } from "@/pages/dashboard/Types";
import AlertModal from "@/pages/dashboard/components/AlertModal";
import ActionBarDelete from "@/pages/dashboard/components/ActionBarDelete";

const AuthorsTable: React.FC<AuthorsTableProps> = ({
  authors,
  searchQuery,
  setCurrentPage,
  currentPage,
  setSearchQuery,
  fetchAuthors,
}) => {
  const { createAuthor, deleteAuthorsBatch } = useAuthorsService();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PostBodyCreateAuthorDto>({ mode: "onChange" });
  const [authorsIDs, setAuthorsIDs] = useState<number[]>([]);
  const hasSelection = authorsIDs.length > 0;
  const indeterminate = hasSelection && authorsIDs.length < authors.length;
  const [isOpenModalAlert, setIsOpenModalAlert] = useState(false);

  const handleAddAuthor = handleSubmit(async (data) => {
    const response = await createAuthor(data);
    if (response.data && response.success) {
      reset();
      toaster.create({
        title: "New author created.",
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

  const deleteAuthors = async () => {
    const response = await deleteAuthorsBatch({ ids: authorsIDs });
    if (response.data && response.success) {
      toaster.create({
        title: response.data.message,
        type: "success",
      });
      fetchAuthors();
      setAuthorsIDs([]);
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
      fetchAuthors();
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
            placeholder="Search by author name..."
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
          <DialogContent colorPalette="teal" bgColor="white">
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
                          value: 50,
                          message: "Name cannot exceed 50 characters",
                        },
                      })}
                    />
                  </Field>
                </Stack>
              </DialogBody>
              <DialogFooter>
                <Button onClick={() => reset()}>Cancel</Button>
                <Button type="submit">Add</Button>
              </DialogFooter>
            </form>
            <DialogCloseTrigger
              color="black"
              _hover={{ bgColor: "teal.300" }}
            />
          </DialogContent>
        </DialogRoot>
      </Flex>
      <Table.Root variant="line" size="sm">
        <Table.Header bg="teal.500">
          <Table.Row borderBottomWidth={3} borderColor="border.emphasized">
            <Table.ColumnHeader width="10%">
              <Checkbox
                borderColor="black"
                borderWidth={1}
                top="1"
                _hover={{ cursor: "pointer" }}
                aria-label="Select all rows"
                checked={
                  indeterminate ? "indeterminate" : authorsIDs.length > 0
                }
                onCheckedChange={(changes) => {
                  setAuthorsIDs(
                    changes.checked ? authors.map((item) => item.id) : []
                  );
                }}
              />
            </Table.ColumnHeader>
            <Table.ColumnHeader width="40%" textAlign="start">
              Author
            </Table.ColumnHeader>
            <Table.ColumnHeader width="40%">ID</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {authors.length > 0 ? (
            authors.map((item) => (
              <Table.Row
                borderBottomWidth={2}
                borderColor="border.emphasized"
                key={item.id}
                data-selected={authorsIDs.includes(item.id) ? "" : undefined}
                bg={authorsIDs.includes(item.id) ? "teal.100" : "white"}
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
                    checked={authorsIDs.includes(item.id)}
                    onCheckedChange={(changes) => {
                      setAuthorsIDs((prev) =>
                        changes.checked
                          ? [...prev, item.id]
                          : authorsIDs.filter((id) => id !== item.id)
                      );
                    }}
                  />
                </Table.Cell>
                <Table.Cell textAlign="start">{item.name}</Table.Cell>
                <Table.Cell>{item.id}</Table.Cell>
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
      <ActionBarDelete
        hasSelection={hasSelection}
        setIsOpenModalAlert={setIsOpenModalAlert}
        setIDs={setAuthorsIDs}
        ids={authorsIDs}
      />
      <AlertModal
        open={isOpenModalAlert}
        setOpen={setIsOpenModalAlert}
        deleteFunction={deleteAuthors}
      />
    </>
  );
};

export default AuthorsTable;
