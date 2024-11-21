import { Navigate } from "react-router-dom";
import {jwtDecode} from "jwt-decode";

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
        state={{ message: "You need to authenticate first" }}
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
          state={{ message: "Session expired. Please log in again." }}
        />
      );
    }
  } catch (error) {
    console.error("Invalid token:", error);
    localStorage.removeItem("token");
    return (
      <Navigate
        to="/login"
        state={{ message: "Invalid session. Please log in again." }}
      />
    );
  }

  return children;
};

export default PrivateRoute;
