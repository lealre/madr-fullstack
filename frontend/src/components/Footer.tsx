import { Text, Box, Flex } from "@chakra-ui/react";
import { FaPython, FaReact } from "react-icons/fa";
import {
  SiChakraui,
  SiFastapi,
  SiSqlalchemy,
  SiTypescript,
} from "react-icons/si";
import { TbHeartCode } from "react-icons/tb";

export default function Footer() {
  return (
    <Box
      as="footer"
      bg="teal.600"
      py={3}
      textAlign="center"
      height="120px"
      mt={8}
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
      alignItems="center"
    >
      <Text fontSize="sm" color="white">
        MADR with
        <TbHeartCode
          size={20}
          style={{
            marginLeft: "5px",
            display: "inline-block",
          }}
        />
      </Text>

      <Text
        fontSize="sm"
        color="white"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <Box display="flex" alignItems="center" mr={2}>
          <FaPython size={25} />
          <SiFastapi size={25} style={{ marginLeft: "8px" }} />
          <SiSqlalchemy size={35} style={{ marginLeft: "8px" }} />
        </Box>
        <Text mx={2}>+</Text>
        <Box display="flex" alignItems="center" ml={2}>
          <SiTypescript size={25} />
          <FaReact size={25} style={{ marginLeft: "8px" }} />
          <SiChakraui size={25} style={{ marginLeft: "8px" }} />
        </Box>
      </Text>
      <Flex paddingLeft={2} justify="flex-start" width="100%">
        <Text fontSize="sm" color="white">
          by{" "}
          <strong>
            <a href="https://github.com/lealre" target="_blank">
              lealre
            </a>
          </strong>
        </Text>
      </Flex>
    </Box>
  );
}
