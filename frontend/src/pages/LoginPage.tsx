import api from "../api.ts";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Header from "../components/Header.tsx";

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

      console.log(err)
      setError('Invalid login credentials');
    }
  };

 return ( <>
    <Header />
    <div
      className="d-flex justify-content-center align-items-center"
      style={{
        backgroundColor: '#f4f3ee',
        minHeight: '70vh',
        padding: '20px',
      }}
      >
      <div className="card p-4" style={{ maxWidth: '400px', width: '100%', backgroundColor: '#bcb8b1' }}>
        <h2 className="text-center mb-4" style={{ color: '#463f3a' }}>
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
              style={{ borderColor: '#8a817c' }}
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
              style={{ borderColor: '#8a817c' }}
              />
          </div>
          <button
            type="submit"
            className="btn w-100"
            style={{
              backgroundColor: '#e0afa0',
              color: '#463f3a',
              borderColor: '#bcb8b1',
            }}
            >
            Login
          </button>
        </form>
        {error && (
          <p className="text-danger text-center mt-3" style={{ color: '#8a817c' }}>
            {error}
          </p>
        )}
      </div>
    </div>
        </>
  );
};