import { Button, Flex, Input, Table } from "@chakra-ui/react";
import { InputGroup } from "./ui/input-group";
import { LuSearch } from "react-icons/lu";
import { GrAdd } from "react-icons/gr";
import React from "react";

interface AuthorsProps {
  id: number;
  name: string;
}

export interface AuthorsTableProps {
  authors: AuthorsProps[];
}

const AuthorsTable: React.FC<AuthorsTableProps> = ({ authors }) => {
  console.log(authors);
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
    </>
  );
};

export default AuthorsTable;
