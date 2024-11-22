import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { Toaster, toaster } from "@/components/ui/toaster";

import api from "../api/api.ts";
import Header from "../components/Header.tsx";

export default function LoginPage() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.message) {
      toaster.create({ title: location.state.message, type: "warning" });
    }
    navigate(location.pathname, { replace: true });
  }, [location.state]);

  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // Make the POST request to the FastAPI backend
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await api.post("/auth/token", formData);
      const { access_token } = response.data;
      localStorage.setItem("token", access_token);

      navigate("/dashboard");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          console.error("No response from the server:", err);
          toaster.create({
            title: "Unable to reach the server. Please try again later.",
            type: "error",
          });
        } else if (err.response.status === 500) {
          console.error("Server error:", err.response);
          toaster.create({
            title: "An internal server error occurred. Please try again later.",
            type: "error",
          });
        } else if (err.response.status === 401 || err.response.status === 400) {
          console.error("Authentication error:", err.response);
          toaster.create({
            title: "Invalid login credentials.",
            type: "error",
          });
        } else {
          console.error("Error:", err.response);
          toaster.create({
            title: "An unexpected error occurred. Please try again.",
            type: "error",
          });
        }
      } else {
        console.error("Non-Axios error:", err);
        toaster.create({
          title: "An unexpected error occurred.",
          type: "error",
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Header />
      <Flex direction="column" justify="center" align="center" height="75vh">
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
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
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
                  setUsername("");
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
        <Toaster />
      </Flex>
    </>
  );
}
