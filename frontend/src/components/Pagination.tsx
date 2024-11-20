import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination";
import { HStack } from "@chakra-ui/react";

export interface PageProps {
  totalResults: number;
  pageSize: number;
  currentPage: number;
  setCurrentPage: (newPage: number) => void;
}

const Pagination: React.FC<PageProps> = (pageProps) => {
  const { totalResults, pageSize, currentPage, setCurrentPage } = pageProps;

  return (
    <PaginationRoot
      count={totalResults}
      pageSize={pageSize}
      defaultPage={1}
      page={currentPage}
      onPageChange={(e) => {
        setCurrentPage(e.page);
      }}
      size="sm"
      color="teal.600"
    >
      <HStack>
        <PaginationPrevTrigger color="black" />
        <PaginationItems color="black" />
        <PaginationNextTrigger color="black" />
      </HStack>
    </PaginationRoot>
  );
};

export default Pagination;
