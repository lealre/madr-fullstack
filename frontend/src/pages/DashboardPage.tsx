import React, { useEffect, useState } from "react";
import { Text, Box, Flex, Container, Center } from "@chakra-ui/react";
import { Tabs } from "@chakra-ui/react";
import { LuUser } from "react-icons/lu";
import { IoBookSharp } from "react-icons/io5";
import { FaUserAlt } from "react-icons/fa";
import api from "../api/apiRoot";
import Header from "../components/Header";
import AuthorsTable, {
  AuthorsTableProps 
} from "../components/AuhtorsTable";
import Pagination, {PageProps} from "../components/Pagination"
import BooksTable, { BooksTableProps } from "../components/BooksTable";

interface TabProps {
  value: string;
}

const Dashboard: React.FC = () => {
  const [authors, setAuthors] = useState<AuthorsTableProps["authors"]>([]);
  const [books, setBooks] = useState<BooksTableProps["books"]>([]);
  const [tab, setTab] = useState<TabProps>({ value: "authors" });

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalResults, setTotalResults] = useState<number>(1);
  const pageSize = 8;

  const [isLoading, setIsLoading] = useState(false);

  const pageProps: PageProps = {
    totalResults: totalResults,
    pageSize: pageSize,
    currentPage: currentPage,
    setCurrentPage: setCurrentPage,
  };

  useEffect(() => {
    fetchAuthors(currentPage);
  }, [currentPage]);

  const fetchAuthors = async (page: number): Promise<void> => {
    if (isLoading) return;
    setIsLoading(true);
    const offset = (page - 1) * pageSize;

    try {
      const response = await api.get(
        `/author/?limit=${pageSize}&offset=${offset}`
      );
      setAuthors(response.data.authors);
      setTotalResults(response.data.total_results);
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
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
    e.value === "authors" ? fetchAuthors(currentPage) : fetchBooks();
  };

  return (
    <>
      <Header />

      <Container maxW="1000px" mx="auto">
        <Flex mt={1} align="center">
          <FaUserAlt size={20} style={{ marginRight: "8px" }} />
          <Text fontSize="lg" alignItems="center">
            test
          </Text>
        </Flex>

        <Box mt={8}>
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
            <Flex direction="column" gap={3}>
              <AuthorsTable authors={authors} />
              <Center>
                <Pagination {...pageProps}></Pagination>
              </Center>
            </Flex>
          ) : (
            <BooksTable books={books} />
          )}
        </Box>
      </Container>
    </>
  );
};

export default Dashboard;
