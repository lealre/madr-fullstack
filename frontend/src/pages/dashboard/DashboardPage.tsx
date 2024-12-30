import React, { useEffect, useState } from "react";
import { Text, Box, Flex, Container, Center } from "@chakra-ui/react";
import { Tabs } from "@chakra-ui/react";
import { LuUser } from "react-icons/lu";
import { IoBookSharp } from "react-icons/io5";
import { FaUserAlt } from "react-icons/fa";
import { Toaster, toaster } from "@/components/ui/toaster";

import Header from "@/components/Header";
import AuthorsTable from "@/pages/dashboard/components/AuhtorsTable";
import { AuthorResponseDto } from "@/dto/AuthorsDto";
import { BookResponseDto } from "@/dto/BooksDto";
import Pagination from "@/pages/dashboard/components/Pagination";
import BooksTable from "@/pages/dashboard/components/BooksTable";
import { PageProps, TabProps } from "@/pages/dashboard/Types";
import useBooksService from "@/api/booksApi";
import useAuthorsService from "@/api/authorsApi";
import useUsersService from "@/api/usersApi";
import { GetCurrentUserDto } from "@/dto/UsersDto";

const Dashboard: React.FC = () => {
  const { getAuthors } = useAuthorsService();
  const { getBooks } = useBooksService();
  const { getCurrentUser } = useUsersService();
  const [currentUser, setCurrentUser] = useState<GetCurrentUserDto | null>();
  const [authors, setAuthors] = useState<AuthorResponseDto[]>([]);
  const [books, setBooks] = useState<BookResponseDto[]>([]);
  const [tab, setTab] = useState<TabProps>({ value: "authors" });
  const [searchQuery, setSearchQuery] = useState("");

  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalResults, setTotalResults] = useState<number>(1);
  const pageSize = 20;

  const [isLoading, setIsLoading] = useState(false);

  const pageProps: PageProps = {
    totalResults: totalResults,
    pageSize: pageSize,
    currentPage: currentPage,
    setCurrentPage: setCurrentPage,
  };

  useEffect(() => {
    fetchAuthors();
    getCurrentUserInfo();
  }, [currentPage]);

  const getCurrentUserInfo = async () => {
    const response = await getCurrentUser();
    if (response.data && response.success) {
      console.log(response.data);
      setCurrentUser(response.data);
    } else {
      toaster.create({
        title: response.error.detail,
        type: "error",
      });
    }
  };

  const fetchAuthors = async (): Promise<void> => {
    if (isLoading) return;
    setIsLoading(true);
    const offset = (currentPage - 1) * pageSize;

    const response = await getAuthors({
      limit: pageSize,
      offset: offset,
      ...(searchQuery && { name: searchQuery }),
    });
    if (response.data && response.success) {
      console.log(response.data);
      setAuthors(response.data.authors);
      const responsetTotalResults = response.data.total_results;
      setTotalResults(responsetTotalResults);
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
    e.value === "authors" ? fetchAuthors() : fetchBooks();
  };

  return (
    <>
      <Header />

      <Flex direction="column" justifyContent="space-between" minHeight="100vh">
        <Container maxW="1000px">
          <Flex mt={1} align="center">
            <FaUserAlt size={20} style={{ marginRight: "8px" }} />
            {currentUser ? (
              <>
                <Text fontSize="lg" alignItems="center">
                  {currentUser.username} ({currentUser.email})
                </Text>
              </>
            ) : (
              <Text></Text>
            )}
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
                <AuthorsTable
                  searchQuery={searchQuery}
                  setSearchQuery={setSearchQuery}
                  authors={authors}
                  fetchAuthors={fetchAuthors}
                />
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

        <Box
          as="footer"
          bg="teal.600"
          py={4}
          textAlign="center"
          height="100px"
          mt={8}
        >
          <Text fontSize="sm">
            © {new Date().getFullYear()} Your Company Name. All rights reserved.
          </Text>
        </Box>
      </Flex>
    </>
  );
};

export default Dashboard;
