import { Button, Flex, Input, Table } from "@chakra-ui/react";
import React from "react";
import { InputGroup } from "./ui/input-group";
import { LuSearch } from "react-icons/lu";
import { GrAdd } from "react-icons/gr";
import { BookResponseDto } from "@/dto/BooksDto";

export interface BooksTableProps {
  books: BookResponseDto[];
}

const BooksTable: React.FC<BooksTableProps> = ({ books }) => {
  return (
    <>
      <Flex gap="4" justify="space-between" mb={2}>
        <InputGroup flex="1" startElement={<LuSearch />}>
          <Input maxW="400px" placeholder="Search authors" />
        </InputGroup>

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
      </Flex>

      {/* Table */}
      <Table.Root key="outline" size="sm" variant="outline">
        <Table.Header bg="teal.500">
          <Table.Row>
            <Table.ColumnHeader>ID</Table.ColumnHeader>
            <Table.ColumnHeader>Title</Table.ColumnHeader>
            <Table.ColumnHeader>Year</Table.ColumnHeader>
            <Table.ColumnHeader textAlign="end">AuthorID</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {books.map((item) => (
            <Table.Row key={item.id}>
              <Table.Cell>{item.id}</Table.Cell>
              <Table.Cell>{item.title}</Table.Cell>
              <Table.Cell>{item.year}</Table.Cell>
              <Table.Cell textAlign="end">{item.author_id}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </>
  );
};

export default BooksTable;
