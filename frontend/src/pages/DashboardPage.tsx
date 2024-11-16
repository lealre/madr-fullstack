import React, { useEffect, useState } from "react";
import { Text, Box, Flex, Container } from "@chakra-ui/react";
import { Tabs } from "@chakra-ui/react";
import { LuUser } from "react-icons/lu";
import { IoBookSharp } from "react-icons/io5";
import { FaUserAlt } from "react-icons/fa";
import api from "../api";
import Header from "../components/Header";
import AuthorsTable, { AuthorsTableProps } from "../components/AuhtorsTable";
import BooksTable, { BooksTableProps } from "../components/BooksTable";

interface TabProps {
  value: string;
}

const Dashboard: React.FC = () => {
  const [authors, setAuthors] = useState<AuthorsTableProps["authors"]>([]);
  const [books, setBooks] = useState<BooksTableProps["books"]>([]);
  const [tab, setTab] = useState<TabProps>({ value: "authors" });

  useEffect(() => {
    fetchAuthors();
  }, []);

  const fetchAuthors = async (): Promise<void> => {
    try {
      const response = await api.get("/author/");
      setAuthors(response.data.authors);
    } catch (err) {
      console.log(err);
    }
  };

  const fetchBooks = async (): Promise<void> => {
    try {
      const response = await api.get("/book/");
      setBooks(response.data.books);
    } catch (err) {
      console.log(err);
    }
  };

  const changeTabView = (e: any) => {
    setTab(e);
    e.value === "authors" ? fetchAuthors() : fetchBooks();
  };

  return (
    <>
      <Header />

      <Container maxW="800px" mx="auto">
        <Flex mt={1} align="center">
          <FaUserAlt size={20} style={{ marginRight: "8px" }} />
          <Text fontSize="lg" alignItems="center">
            test
          </Text>
        </Flex>

        <Box mt={8}>
          {/* Dashboard + Tabs */}
          <Flex borderBottom="1px solid black" mb={3} justify="space-between">
            <Text fontWeight="semibold" fontSize="40px" mb={0}>
              Dashboard Area
            </Text>

            <Tabs.Root
              defaultValue="authors"
              onValueChange={(e) => changeTabView(e)}
            >
              <Tabs.List
                display="flex"
                alignItems="flex-end"
                borderBottom="0px"
                height="100%"
              >
                <Tabs.Trigger
                  value="authors"
                  _selected={{
                    color: "black",
                    fontWeight: "bold",
                    borderBottom: "3px solid teal",
                  }}
                >
                  <LuUser />
                  Authors
                </Tabs.Trigger>
                <Tabs.Trigger
                  value="books"
                  _selected={{
                    color: "black",
                    fontWeight: "bold",
                    borderBottom: "3px solid teal",
                  }}
                >
                  <IoBookSharp />
                  Books
                </Tabs.Trigger>
              </Tabs.List>
            </Tabs.Root>
          </Flex>

          {tab.value === "authors" ? (
            <AuthorsTable authors={authors} />
          ) : (
            <BooksTable books={books} />
          )}
        </Box>
      </Container>
    </>
  );
};

export default Dashboard;
