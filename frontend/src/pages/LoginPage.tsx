import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import axios from "axios";

import api from "../api.ts";
import Header from "../components/Header.tsx";
import AlertMessage from "../components/AlertMessage";

export default function LoginPage() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.error) {
      setError(location.state.error);
    }

    navigate(location.pathname, { replace: true });

    const timer = setTimeout(() => {
      return setError("");
    }, 5000);

    return () => clearTimeout(timer);
  }, [location.state]);

  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();

    try {
      // Make the POST request to the FastAPI backend
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await api.post("/auth/token", formData);
      const { access_token } = response.data;
      console.log(response.data);
      // Save the JWT token in localStorage
      localStorage.setItem("token", access_token);

      // Navigate to the dashboard after successful login
      navigate("/dashboard");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          console.error("No response from the server:", err);
          setError("Unable to reach the server. Please try again later.");
        } else if (err.response.status === 500) {
          console.error("Server error:", err.response);
          setError(
            "An internal server error occurred. Please try again later."
          );
        } else if (err.response.status === 401 || err.response.status === 400) {
          console.error("Authentication error:", err.response);
          setError("Invalid login credentials.");
        } else {
          console.error("Error:", err.response);
          setError("An unexpected error occurred. Please try again.");
        }
      } else {
        console.error("Non-Axios error:", err);
        setError("An unexpected error occurred.");
      }
    }
  };

  return (
    <>
      <Header />
      <Flex direction="column" justify="center" align="center" height="75vh">
        <form onSubmit={handleLogin}>
          <Card.Root maxW="sm" colorPalette="teal" layerStyle="fill.subtle">
            <Card.Header>
              <Card.Title>Sign up</Card.Title>
              <Card.Description color="teal.600">
                Fill in the form below to create an account
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
              <Button type="submit">Sign in</Button>
            </Card.Footer>
          </Card.Root>
        </form>
        {error && <AlertMessage type="error" message={error} />}
      </Flex>
    </>
  );
}
