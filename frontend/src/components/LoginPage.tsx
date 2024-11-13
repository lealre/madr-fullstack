import api from "../api.ts";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();

    try {
      // Make the POST request to the FastAPI backend
      const formData = new URLSearchParams();
      formData.append("username", username); // Assuming 'email' is your username
      formData.append("password", password);

      const response = await api.post("/auth/token", formData);
      const { access_token } = response.data;
      console.log(response.data)
      // Save the JWT token in localStorage
      localStorage.setItem("token", access_token);

      // Navigate to the dashboard after successful login
      navigate('/dashboard');
    } catch (err) {
      // Handle login error
      console.log(err)
      setError('Invalid login credentials');
    }
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <input
          type="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Login</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};