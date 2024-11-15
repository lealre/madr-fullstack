import React from "react";
import { Box, Flex, Heading, Button, Link } from "@chakra-ui/react";
import { useLocation, useNavigate, Link as RouterLink } from "react-router-dom";

const Header: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token"); // Remove the token to log out
    navigate("/", { state: { message: "You have successfully logged out." } }); // Redirect to login page
  };

  return (
    <Box bg="teal.600" py={2}>
      <Flex
        justify="space-between"
        align="center"
        maxWidth="1200px"
        mx="auto"
        px={4}
      >
        <Heading size="lg" color="white" margin={0}>
          <Link
            style={{ textDecoration: "none" }}
            variant="plain"
            color="white"
            _hover={{ color: "gray.200" }}
          >
            MADR
          </Link>
        </Heading>

        {/* Conditionally render Login or Logout based on authentication status */}
        {isAuthenticated ? (
          <Button
            variant="plain" // Makes the button look like a link
            color="white" // Sets the text color to white
            fontSize="18px" // Sets the font size
            _hover={{ textDecoration: "none", color: "gray.200" }} // Removes underline and changes color on hover
            onClick={handleLogout}
          >
            Logout
          </Button>
        ) : (
          location.pathname !== "/login" && (
            <RouterLink to="/login">
              <Link
                variant="plain"
                color="white"
                fontSize="18px"
                _hover={{ textDecoration: "none", color: "gray.200" }}
              >
                Login
              </Link>
            </RouterLink>
          )
        )}
      </Flex>
    </Box>
  );
};

export default Header;
