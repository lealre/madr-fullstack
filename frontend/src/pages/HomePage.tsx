import { useLocation, useNavigate } from "react-router-dom";
import AlertMessage from "../components/AlertMessage";

import Header from "../components/Header";
import { useEffect, useState } from "react";

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
      <div className="container text-center mt-5">
        <h1 style={{ color: "#463f3a" }}>Welcome to MADR App!</h1>
        <p style={{ color: "#8a817c" }}>This is an introduction to the app.</p>
        {message && <AlertMessage type="info" message={message} />}
      </div>
    </>
  );
};

export default HomePage;
