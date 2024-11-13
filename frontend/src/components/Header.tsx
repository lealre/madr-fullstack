import React from "react";
import { Link, useLocation } from "react-router-dom";

const Header: React.FC = () => {
  const location = useLocation();
  return (
    <header style={{ backgroundColor: "#463f3a", padding: "10px 20px" }}>
      <div className="container-fluid d-flex justify-content-between align-items-center">
        <h1 style={{ color: "#f4f3ee", margin: 0 }}>
          <Link
            to="/"
            style={{
              color: "inherit",
              cursor: "pointer",
              textDecoration: "none",
            }}
          >
            MADR
          </Link>
        </h1>
        {/* Conditionally render the Login link based on the current route */}
        {location.pathname !== "/login" && (
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
        )}
      </div>
    </header>
  );
};

export default Header;
