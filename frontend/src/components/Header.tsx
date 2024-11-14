import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

const Header: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token"); // Remove the token to log out
    navigate("/", { state: { message: "You have successfully logged out." } }); // Redirect to login page
  };

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
        {/* Conditionally render Login or Logout based on authentication status */}
        {isAuthenticated ? (
          <button
            onClick={handleLogout}
            style={{
              backgroundColor: "transparent",
              border: "none",
              color: "#f4f3ee",
              cursor: "pointer",
              fontSize: "18px",
            }}
          >
            Logout
          </button>
        ) : (
          location.pathname !== "/login" && (
            <Link
              to="/login"
              style={{
                color: "#f4f3ee",
                textDecoration: "none",
                fontSize: "18px",
              }}
            >
              Login
            </Link>
          )
        )}
      </div>
    </header>
  );
};

export default Header;
