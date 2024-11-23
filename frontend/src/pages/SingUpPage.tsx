import { Box, Button, Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { useForm } from "react-hook-form";
import Header from "../components/Header";
import { useNavigate } from "react-router-dom";

import useUsersService from "@/api/usersApi";
import { Toaster, toaster } from "@/components/ui/toaster";
import { SingUpRequestDto } from "@/dto/UsersDto";

const singUpPage = () => {
  const { createUser } = useUsersService();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SingUpRequestDto>({ mode: "onChange" });
  const navigate = useNavigate();

  const handleAddAuthor = handleSubmit(async (data) => {
    const response = await createUser(data);
    if (response.data && response.success) {
      navigate("/login", {
        state: {
          message: {
            title:
              "User created successfully! Enter your credentials to log in",
            type: "success",
          },
        },
      });
    } else {
      if (Array.isArray(response.error)) {
        response.error.forEach((errorMsg: string) => {
          toaster.create({
            title: errorMsg,
            type: "error",
          });
        });
      } else {
        toaster.create({
          title: response.error?.detail ?? "An error occurred",
          type: "error",
        });
      }
    }
  });

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
          height="75vh"
          flex="1"
          marginTop={1}
        >
          <form onSubmit={handleAddAuthor}>
            <Card.Root
              w="md"
              colorPalette="teal"
              layerStyle="fill.subtle"
              variant="elevated"
            >
              <Card.Header>
                <Card.Title>Sign up</Card.Title>
                <Card.Description color="teal.600">
                  Fill in the form below to create an account
                </Card.Description>
              </Card.Header>
              <Card.Body>
                <Stack gap="4" w="full">
                  <Field
                    label="Username"
                    invalid={!!errors.username}
                    errorText={errors.username?.message}
                  >
                    <Input
                      {...register("username", {
                        required: "Username is required",
                        maxLength: {
                          value: 20,
                          message: "Name cannot exceed 20 characters",
                        },
                      })}
                    />
                  </Field>
                  <Field
                    label="Email"
                    invalid={!!errors.email}
                    errorText={errors.email?.message}
                  >
                    <Input
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
                      type="password"
                      {...register("password", {
                        required: "Password is required",
                      })}
                    />
                  </Field>
                </Stack>
              </Card.Body>
              <Card.Footer justifyContent="flex-end">
                <Button onClick={() => reset()}>Cancel</Button>
                <Button type="submit">Sign in</Button>
              </Card.Footer>
            </Card.Root>
          </form>
        </Flex>
        <Toaster />
      </Flex>
    </>
  );
};

export default singUpPage;
