import { Button, Card, Flex, Input, Stack } from "@chakra-ui/react";
import { Field } from "@/components/ui/field";
import { useForm } from "react-hook-form";
import Header from "../components/Header";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import api from "../api/api.ts";
import { Toaster, toaster } from "@/components/ui/toaster";

interface SingUpFormProps {
  username: string;
  email: string;
  password: string;
}

const singUpPage = () => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<SingUpFormProps>();
  const navigate = useNavigate();

  const handleAddAuthor = handleSubmit(async (data) => {
    try {
      await api.post("/users/", data);
      navigate("/login", {
        state: {
          message: "Account created successfully! Please log in.",
        },
      });
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          console.error("No response from the server:", err);
          toaster.create({title: "Unable to reach the server. Please try again later.", type: "error"});
        } else if (err.response.status === 500) {
          console.error("Server error:", err.response);
          toaster.create(
            {title: "An internal server error occurred. Please try again later.", type: "error"}
          );
        } else if (err.response.status === 400) {
          console.error("Credentials already exists", err.response);
          toaster.create({title: err.response.data.detail, type: "error"});
        } else {
          console.error("Error:", err.response);
          toaster.create({title: "An unexpected error occurred. Please try again.", type: "error"});
        }
      } else {
        console.error("Non-Axios error:", err);
        toaster.create({title: "An unexpected error occurred.", type: "error"});
      }
    }
  });

  return (
    <>
      <Header />
      <Flex direction="column" justify="center" align="center" height="75vh">
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
              <Button
                onClick={() => reset()
                }
              >
                Cancel
              </Button>
              <Button type="submit">Sign in</Button>
            </Card.Footer>
          </Card.Root>
        </form>
      </Flex>
      <Toaster/>
    </>
  );
};

export default singUpPage;
