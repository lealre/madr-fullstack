import { useLocation, useNavigate } from "react-router-dom";
import AlertMessage from "../components/AlertMessage";
import Header from "../components/Header";
import { useEffect, useState } from "react";
import { Box, Flex, Text } from "@chakra-ui/react";

const HomePage: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.message) {
      setMessage(location.state.message);
    }

    navigate(location.pathname, { replace: true });

    const timer = setTimeout(() => {
      return setMessage("");
    }, 5000);

    return () => clearTimeout(timer);
  }, [location.state]);

return (
  <>
    <Header />
    <Box mt={8} justifyContent="center">
      <Flex
        maxWidth="1500px"
        direction="column"
        alignItems="center"
        textAlign="center"
      >
        <Text textStyle="5xl">Welcome to MADR App!</Text>
      </Flex>
    </Box>

    {message && <AlertMessage type="info" message={message} />}
  </>
);
};

export default HomePage;
