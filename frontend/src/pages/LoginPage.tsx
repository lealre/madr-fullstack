import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

import api from "../api.ts";
import Header from "../components/Header.tsx";

export default function LoginPage() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [error, setError] = useState<string>();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.state?.error) {
      setError(location.state.error);
    }

    navigate(location.pathname, { replace: true });

    const timer = setTimeout(() => {
      return setError("");
    }, 5000);

    return () => clearTimeout(timer);
  }, [location.state]);

  const handleLogin = async (
    e: React.FormEvent<HTMLFormElement>
  ): Promise<void> => {
    e.preventDefault();

    try {
      // Make the POST request to the FastAPI backend
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await api.post("/auth/token", formData);
      const { access_token } = response.data;
      console.log(response.data);
      // Save the JWT token in localStorage
      localStorage.setItem("token", access_token);

      // Navigate to the dashboard after successful login
      navigate("/dashboard");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        if (!err.response) {
          console.error("No response from the server:", err);
          setError("Unable to reach the server. Please try again later.");
        } else if (err.response.status === 500) {
          console.error("Server error:", err.response);
          setError(
            "An internal server error occurred. Please try again later."
          );
        } else if (err.response.status === 401 || err.response.status === 400) {
          console.error("Authentication error:", err.response);
          setError("Invalid login credentials.");
        } else {
          console.error("Error:", err.response);
          setError("An unexpected error occurred. Please try again.");
        }
      } else {
        console.error("Non-Axios error:", err);
        setError("An unexpected error occurred.");
      }
    }
  };

  return (
    <>
      <Header />
      <div
        className="d-flex justify-content-center align-items-center"
        style={{
          backgroundColor: "#f4f3ee",
          minHeight: "70vh",
          padding: "20px",
        }}
      >
        <div
          className="card p-4"
          style={{
            maxWidth: "400px",
            width: "100%",
            backgroundColor: "#bcb8b1",
          }}
        >
          <h2 className="text-center mb-4" style={{ color: "#463f3a" }}>
            Login
          </h2>
          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                required
                style={{ borderColor: "#8a817c" }}
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                style={{ borderColor: "#8a817c" }}
              />
            </div>
            <button
              type="submit"
              className="btn w-100"
              style={{
                backgroundColor: "#e0afa0",
                color: "#463f3a",
                borderColor: "#bcb8b1",
              }}
            >
              Login
            </button>
          </form>
        </div>
        {error && (
          <div
            className="alert alert-danger alert-dismissible fade show"
            role="alert"
            style={{
              position: "fixed",
              bottom: "20px",
              left: "50%",
              transform: "translateX(-50%)",
              zIndex: 1000,
              animation: "slideUp 0.3s ease-out forwards"
            }}
          >
            {error}
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
              onClick={() => setError("")}
            ></button>
          </div>
        )}
      </div>
    </>
  );
}
