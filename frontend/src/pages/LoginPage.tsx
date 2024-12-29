import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useLocation, useNavigate } from "react-router-dom";
import { Box, Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { Button } from "@/components/ui/button";
import { Toaster, toaster } from "@/components/ui/toaster";

import Header from "@/components/Header.tsx";
import useAuthService from "@/api/authApi.ts";
import { SignInDto } from "@/dto/UsersDto";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const location = useLocation();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SignInDto>({ mode: "onChange" });

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

  const handleLogin = handleSubmit(async (data) => {
    if (isLoading) return;
    setIsLoading(true);

    const response = await signInUser({
      email: data.email,
      password: data.password,
    });
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
  });

  return (
    <>
      <Flex direction="column" minHeight="100vh" gap={1} bg="teal.50">
        <Box>
          <Header />
        </Box>

        <Flex direction="column" justify="center" align="center" flex="1">
          <form onSubmit={handleLogin}>
            <Card.Root
              w="sm"
              // bgColor="teal.500"
              borderWidth={1}
              shadow="xl"
              colorPalette="teal"
              variant="elevated"
              borderColor="gray.300"
            >
              <Card.Header>
                <Card.Title>Login</Card.Title>
                <Card.Description color="black">
                  Fill in the form below to login
                </Card.Description>
              </Card.Header>
              <Card.Body>
                <Stack gap="4" w="full">
                  <Field
                    label="Email"
                    invalid={!!errors.email}
                    errorText={errors.email?.message}
                  >
                    <Input
                      borderColor="teal.500"
                      {...register("email", {
                        required: "Email is required",
                        maxLength: {
                          value: 30,
                          message: "Email cannot exceed 30 characters",
                        },
                      })}
                    />
                  </Field>
                  <Field
                    label="Password"
                    invalid={!!errors.password}
                    errorText={errors.password?.message}
                  >
                    <Input
                      borderColor="teal.500"
                      type="password"
                      {...register("password", {
                        required: "Password is required",
                      })}
                    />
                  </Field>
                </Stack>
              </Card.Body>
              <Card.Footer justifyContent="flex-end">
                <Button loading={isLoading} onClick={() => reset()}>
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
