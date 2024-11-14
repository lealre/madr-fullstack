import { Link, useLocation, useNavigate } from "react-router-dom";


import Header from "../components/Header";
import { useEffect, useState } from "react";

const HomePage: React.FC = () => {
  const [message, setMessage] = useState<string>('')
  const location = useLocation()
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
        <p style={{ color: "#8a817c" }}>
          This is an introduction to the app. Please login to continue to your
          dashboard.
        </p>
        <Link
          to="/login"
          className="btn"
          style={{
            backgroundColor: "#e0afa0",
            color: "#463f3a",
            borderColor: "#bcb8b1",
            textDecoration: "none",
          }}
        >
          Login
        </Link>
        {message && (
          <div
            className="alert-modal"
            style={{
              position: "fixed",
              bottom: "20px",
              left: "50%",
              transform: "translateX(-50%)",
              maxWidth: "400px",
              width: "90%",
              backgroundColor: "#d4edda",
              color: "#155724",
              borderColor: "#c3e6cb",
              padding: "15px",
              borderRadius: "5px",
              boxShadow: "0 2px 10px rgba(0, 0, 0, 0.2)",
              textAlign: "center",
              zIndex: 1000,
            }}
          >
            {message}
          </div>
        )}
      </div>
    </>
  );
};


export default HomePage;
