import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Flex, Text } from "@chakra-ui/react";
import { Toaster, toaster } from "@/components/ui/toaster";

import Header from "../components/Header";

const HomePage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.message) {
      toaster.create({
        title: location.state.message.title,
        type: location.state.message.type,
      });
    }

    navigate(location.pathname, { replace: true });
  }, [location.state]);

  return (
    <>
      <Header />
      <Container mt={8} justifyContent="center">
        <Flex
          maxWidth="1500px"
          direction="column"
          alignItems="center"
          textAlign="center"
        >
          <Text textStyle="5xl">Welcome to MADR App!</Text>
          <Text textStyle="xl">Add links here to login or logout</Text>
          <Text textStyle="xl">Add here Sectiojn about the project</Text>
        </Flex>
      </Container>
      <Toaster />
    </>
  );
};

export default HomePage;
