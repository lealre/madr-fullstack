import React from "react";
import { Box, Flex, Heading, Button, Link } from "@chakra-ui/react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  DrawerBackdrop,
  DrawerBody,
  DrawerCloseTrigger,
  DrawerContent,
  DrawerHeader,
  DrawerRoot,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { ImMenu } from "react-icons/im";

const Header: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/", {
      state: {
        message: { title: "You have successfully logged out.", type: "info" },
      },
    });
  };

  return (
    <Box bg="teal.600" p={2} height="full">
      <Flex
        justify="space-between"
        align="center"
        maxWidth="1400px"
      >
        <Heading size="3xl" color="white" margin={0}>
          <Button
            asChild
            variant="plain"
            color="white"
            fontSize="3xl"
            _hover={{ color: "gray.200", textDecoration: "none" }}
            focusRing="none"
          >
            <Link href="/">MADR</Link>
          </Button>
        </Heading>

        <DrawerRoot size="xs" initialFocusEl={() => null}>
          <DrawerBackdrop />
          <DrawerTrigger asChild color="white">
            <Button
              variant="outline"
              size="sm"
              borderWidth={2}
              borderColor="white"
              _hover={{ backgroundColor: "teal.500" }}
            >
              <ImMenu />
            </Button>
          </DrawerTrigger>
          <DrawerContent bg="teal.600">
            <DrawerHeader>
              <DrawerTitle></DrawerTitle>
            </DrawerHeader>
            <DrawerBody>
              <Flex
                direction="column"
                justify="flex-start"
                alignItems="flex-start"
              >
                {isAuthenticated ? (
                  <Button
                    variant="plain"
                    color="white"
                    fontSize="18px"
                    _hover={{ textDecoration: "none", color: "gray.200" }}
                    _focus={{
                      textDecoration: "none",
                      outline: "none",
                      color: "gray.100",
                    }}
                    onClick={handleLogout}
                  >
                    Logout
                  </Button>
                ) : (
                  location.pathname !== "/login" && (
                    <Button
                      variant="plain"
                      color="white"
                      fontSize="18px"
                      _hover={{ textDecoration: "none", color: "gray.200" }}
                      _focus={{
                        textDecoration: "none",
                        outline: "none",
                        color: "gray.100",
                      }}
                      asChild
                    >
                      <Link href="/login">Login</Link>
                    </Button>
                  )
                )}

                <Button
                  variant="plain"
                  color="white"
                  fontSize="18px"
                  _hover={{ textDecoration: "none", color: "gray.200" }}
                  _focus={{
                    textDecoration: "none",
                    outline: "none",
                    color: "gray.100",
                  }}
                  asChild
                >
                  <Link href="/singup">Sing Up</Link>
                </Button>
              </Flex>
            </DrawerBody>
            <DrawerCloseTrigger _hover={{ backgroundColor: "teal.500" }} />
          </DrawerContent>
        </DrawerRoot>
      </Flex>
    </Box>
  );
};

export default Header;
