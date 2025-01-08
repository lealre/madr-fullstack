import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Flex, Text } from "@chakra-ui/react";
import { Toaster, toaster } from "@/components/ui/toaster";

import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { ImBooks } from "react-icons/im";

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
      <Flex direction="column" justifyContent="space-between" minHeight="90vh">
        <Container mt={8} justifyContent="center">
          <Flex
            maxWidth="1500px"
            direction="column"
            alignItems="center"
            textAlign="center"
          >
            <Flex direction="row" textAlign="center" alignItems="self-end">
              <ImBooks
                style={{
                  marginRight: "20px",
                  verticalAlign: "middle",
                  width: "50px",
                  height: "50px",
                }}
              />
              <Text textStyle="5xl">Homepage</Text>
              <ImBooks
                size={50}
                style={{
                  marginLeft: "20px",
                  verticalAlign: "middle",
                  width: "50px",
                  height: "50px",
                }}
              />
            </Flex>
          </Flex>
        </Container>
      </Flex>
      <Toaster />
      <Footer />
    </>
  );
};

export default HomePage;
