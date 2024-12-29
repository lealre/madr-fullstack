import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { Button } from "@/components/ui/button";
import { Toaster, toaster } from "@/components/ui/toaster";

import Header from "../components/Header.tsx";
import useAuthService from "@/api/authApi.ts";

export default function LoginPage() {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const location = useLocation();
  const navigate = useNavigate();

  const { signInUser } = useAuthService();

  useEffect(() => {
    if (location.state?.message) {
      toaster.create({
        title: location.state.message.title,
        type: location.state.message.type,
      });
    }
    navigate(location.pathname, { replace: true });
  }, [location.state]);

  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();
    if (isLoading) return;
    setIsLoading(true);

    const response = await signInUser({ email: email, password: password });
    if (response.data && response.success) {
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } else {
      toaster.create({
        title: response.error?.detail ?? "An error occurred",
        type: "error",
      });
    }

    setIsLoading(false);
  };

  return (
    <>
      <Flex direction="column" minHeight="100vh">
        <Box>
          <Header />
        </Box>

        <Flex
          direction="column"
          justify="center"
          align="center"
          marginTop={1}
          flex="1" // Takes up the remaining space after Header
        >
          <form onSubmit={handleLogin}>
            <Card.Root
              w="sm"
              colorPalette="teal"
              layerStyle="fill.subtle"
              variant="elevated"
            >
              <Card.Header>
                <Card.Title>Sign In</Card.Title>
                <Card.Description color="teal.600">
                  Fill in the form below to login
                </Card.Description>
              </Card.Header>
              <Card.Body>
                <Stack gap="4" w="full">
                  <Field label="Email">
                    <Input
                      borderColor="teal.300"
                      type="text"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </Field>
                  <Field label="Password">
                    <Input
                      borderColor="teal.300"
                      required
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </Field>
                </Stack>
              </Card.Body>
              <Card.Footer justifyContent="flex-end">
                <Button
                  onClick={() => {
                    setEmail("");
                    setPassword("");
                  }}
                >
                  Cancel
                </Button>
                <Button type="submit" loading={isLoading}>
                  Sign in
                </Button>
              </Card.Footer>
            </Card.Root>
          </form>
        </Flex>
        <Toaster />
      </Flex>
    </>
  );
}
