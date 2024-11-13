import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import Dashboard from "../pages/DashboardPage";
import HomePage from "../pages/HomePage";
import PrivateRoute from "../routes/PrivateRoute";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        {/* Public route */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />

        {/* Private route */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        {/* If no match, redirect to login */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
