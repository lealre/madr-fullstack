import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import LoginPage from "@/pages/LoginPage";
import Dashboard from "@/pages/dashboard/DashboardPage";
import HomePage from "@/pages/HomePage";
import SingUpPage from "@/pages/SingUpPage";
import PrivateRoute from "@/routes/PrivateRoute";
import Demo from "@/pages/TestPage";

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SingUpPage />} />
        <Route path="/test" element={<Demo />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
