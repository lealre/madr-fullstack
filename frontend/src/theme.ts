import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const customConfig = defineConfig({
  globalCss: {
    html: {
      backgroundColor: "white",
    },
    body: {
      backgroundColor: "white",
      color: "black",
      margin: "0 auto",
    },
  },
  theme: {
    breakpoints: {
      custom_sm: "550px",
      custom_md: "900px",
      // custom_lg: "62em",
      // custom_xl: "80em",
    },
  },
});

export const system = createSystem(defaultConfig, customConfig);
