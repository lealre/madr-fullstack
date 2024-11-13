import { Link } from "react-router-dom";

import Header from "../components/Header";

const HomePage: React.FC = () => {
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
      </div>
      </>
  );
};

export default HomePage;
