import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

interface DecodedToken {
  exp: number;
}

const PrivateRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const token = localStorage.getItem("token");

  // Check if the token exists
  if (!token) {
    return (
      <Navigate
        to="/login"
        state={{
          message: { title: "You need to authenticate first", type: "warning" },
        }}
      />
    );
  }

  try {
    const decodedToken = jwtDecode<DecodedToken>(token);

    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
    if (decodedToken.exp < currentTime) {
      localStorage.removeItem("token");
      return (
        <Navigate
          to="/login"
          state={{
            message: {
              title: "Session expired. Please log in again.",
              type: "warning",
            },
          }}
        />
      );
    }
  } catch (error) {
    console.error("Invalid token:", error);
    localStorage.removeItem("token");
    return (
      <Navigate
        to="/login"
        state={{
          message: {
            title: "Invalid session. Please log in again.",
            type: "warining",
          },
        }}
      />
    );
  }

  return children;
};

export default PrivateRoute;
