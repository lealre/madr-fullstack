import React, { useEffect, useState } from "react";
import { Text, Box, Flex, Container, Center } from "@chakra-ui/react";
import { Tabs } from "@chakra-ui/react";
import { LuUser } from "react-icons/lu";
import { IoBookSharp } from "react-icons/io5";
import { FaUserAlt } from "react-icons/fa";
import useAuthorsService from "@/api/authorsApi";
import Header from "../components/Header";
import AuthorsTable from "../components/AuhtorsTable";
import {AuthorResponseDto} from "@/dto/AuthorsDto"
import { BookResponseDto } from "@/dto/BooksDto";
import Pagination, { PageProps } from "../components/Pagination";
import BooksTable from "../components/BooksTable";
import { Toaster, toaster } from "@/components/ui/toaster";
import useBooksService from "@/api/booksApi";

interface TabProps {
  value: string;
}

const Dashboard: React.FC = () => {
  const { getAuthors } = useAuthorsService();
  const { getBooks } = useBooksService();
  const [authors, setAuthors] = useState<AuthorResponseDto[]>([]);
  const [books, setBooks] = useState<BookResponseDto[]>([]);
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

    const response = await getAuthors({ limit: pageSize, offset: offset });
    if (response.data && response.success) {
      setAuthors(response.data.authors);
      const totalResults = response.data.total_results;
      setTotalResults(totalResults);
    } else {
      toaster.create({
        title: response.error.detail,
        type: "error",
      });
      setAuthors([]);
    }

    setIsLoading(false);
  };

  const fetchBooks = async (): Promise<void> => {
    const response = await getBooks();
    if (response.data && response.success) {
      setBooks(response.data.books);
    } else {
      toaster.create({
        title: response.error.detail,
        type: "error",
      });
      setBooks([]);
    }
  };

  const changeTabView = (e: TabProps) => {
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
        <Toaster />
      </Container>
    </>
  );
};

export default Dashboard;
