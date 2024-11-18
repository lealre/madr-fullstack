import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const customConfig = defineConfig({
  globalCss: {
    "body": {
      backgroundColor: "white",
      color: "black", 
    },
  },
});

export const system = createSystem(defaultConfig, customConfig);
