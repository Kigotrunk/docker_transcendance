import React, { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await axios.post("http://localhost:8000/api/login/", {
        email: username,
        password: password,
      });
      login(response.data.user, response.data.access, response.data.refresh);
      navigate("/home");
    } catch (err) {
      console.error(err);
      setError("Invalid Credentials");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
      {error && <p>{error}</p>}
      <Link to={"/register"}>Register</Link>
      <br />
      <Link to={"/reset_password"}>Reset Password</Link>
    </div>
  );
};

export default Login;
