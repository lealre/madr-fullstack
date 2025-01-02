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
  const { getCurrentUser } = useUsersService();
  const [currentUser, setCurrentUser] = useState<GetCurrentUserDto | null>();

  const { getAuthors } = useAuthorsService();
  const [authors, setAuthors] = useState<AuthorResponseDto[]>([]);
  const [authorsTotalResults, setAuthorsTotalResults] = useState<number>(1);
  const [authorsSearchQuery, setAuthorsSearchQuery] = useState("");
  const [authorsCurrentPage, setAuthorsCurrentPage] = useState<number>(1);

  const { getBooks } = useBooksService();
  const [books, setBooks] = useState<BookResponseDto[]>([]);
  const [booksTotalResults, setBooksTotalResults] = useState<number>(1);
  const [booksSearchQuery, setBooksSearchQuery] = useState("");
  const [booksCurrentPage, setBooksCurrentPage] = useState<number>(1);

  const [tab, setTab] = useState<TabProps>({ value: "authors" });
  const [isLoading, setIsLoading] = useState(false);
  const pageSize = 20;

  const authorsPageProps: PageProps = {
    totalResults: authorsTotalResults,
    pageSize: pageSize,
    currentPage: authorsCurrentPage,
    setCurrentPage: setAuthorsCurrentPage,
  };

  const booksPageProps: PageProps = {
    totalResults: booksTotalResults,
    pageSize: pageSize,
    currentPage: booksCurrentPage,
    setCurrentPage: setBooksCurrentPage,
  };

  useEffect(() => {
    getCurrentUserInfo();
  }, []);

  useEffect(() => {
    fetchAuthors();
  }, [authorsCurrentPage]);

  useEffect(() => {
    fetchBooks();
  }, [booksCurrentPage]);

  const getCurrentUserInfo = async () => {
    const response = await getCurrentUser();
    if (response.data && response.success) {
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
    const offset = (authorsCurrentPage - 1) * pageSize;

    const response = await getAuthors({
      limit: pageSize,
      offset: offset,
      ...(authorsSearchQuery && { name: authorsSearchQuery }),
    });
    if (response.data && response.success) {
      setAuthors(response.data.authors);
      const responsetTotalResults = response.data.total_results;
      setAuthorsTotalResults(responsetTotalResults);
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
    if (isLoading) return;
    setIsLoading(true);
    const offset = (booksCurrentPage - 1) * pageSize;

    const response = await getBooks({
      limit: pageSize,
      offset: offset,
      ...(booksSearchQuery && { title: booksSearchQuery }),
    });
    if (response.data && response.success) {
      setBooks(response.data.books);
      const responsetTotalResults = response.data.total_results;
      setBooksTotalResults(responsetTotalResults);
    } else {
      toaster.create({
        title: response.error.detail,
        type: "error",
      });
      setBooks([]);
    }

    setIsLoading(false);
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
                  searchQuery={authorsSearchQuery}
                  setSearchQuery={setAuthorsSearchQuery}
                  setCurrentPage={setAuthorsCurrentPage}
                  currentPage={authorsCurrentPage}
                  authors={authors}
                  fetchAuthors={fetchAuthors}
                />
                <Center>
                  <Pagination {...authorsPageProps}></Pagination>
                </Center>
              </Flex>
            ) : (
              <Flex direction="column" gap={3}>
                <BooksTable
                  searchQuery={booksSearchQuery}
                  setSearchQuery={setBooksSearchQuery}
                  setCurrentPage={setBooksCurrentPage}
                  currentPage={booksCurrentPage}
                  books={books}
                  authors={authors}
                  fetchBooks={fetchBooks}
                />
                <Center>
                  <Pagination {...booksPageProps}></Pagination>
                </Center>
              </Flex>
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
