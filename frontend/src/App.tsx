import { Provider } from "./components/ui/provider";

import AppRouter from "./routes/AppRouter";


function App() {
  return (
    <>
      <Provider >
        <AppRouter />
      </Provider>
    </>
  );
}

export default App;
