import React from "react";
import { Stack} from "@chakra-ui/react";
import { Alert } from "@/components/ui/alert";


interface AlertMessageProps {
  type: "success" | "error" | "warning" | "info";
  message: string;
}

const AlertMessage: React.FC<AlertMessageProps> = ({ type, message }) => {
  return (
    <Stack
      position="fixed"
      bottom="20px"
      left="50%"
      transform="translateX(-50%)"
      zIndex="1000"
      width="90%"
      maxWidth="400px"
    >
      <Alert status={type} borderRadius="5px">
        {message}
      </Alert>
    </Stack>
  );
};

export default AlertMessage;
