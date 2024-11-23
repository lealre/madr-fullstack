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
import {
  ActionBarContent,
  ActionBarRoot,
  ActionBarSelectionTrigger,
  ActionBarSeparator,
} from "@/components/ui/action-bar";
import { Toaster, toaster } from "@/components/ui/toaster";
import { Checkbox } from "@/components/ui/checkbox";
import { useForm } from "react-hook-form";
import useRootApiService from "@/api/authorsApi";
import { AuthorResponseDto, PostBodyCreateAuthorDto } from "@/dto/AuthorsDto";


interface AuthorsTableProps {
  authors: AuthorResponseDto[];
}

const AuthorsTable: React.FC<AuthorsTableProps> = ({ authors }) => {
  const { createAuthor } = useRootApiService();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PostBodyCreateAuthorDto>({ mode: "onChange" });

  const [selection, setSelection] = useState<number[]>([]);
  const hasSelection = selection.length > 0;
  const indeterminate = hasSelection && selection.length < authors.length;

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
            <DialogCloseTrigger />
          </DialogContent>
        </DialogRoot>
      </Flex>

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
                checked={indeterminate ? "indeterminate" : selection.length > 0}
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
      <Toaster />
    </>
  );
};

export default AuthorsTable;
