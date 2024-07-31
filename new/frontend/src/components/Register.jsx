import React from "react";
import { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import "../css/register.css";

const Register = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [message, setMessage] = useState("");

  const navigate = useNavigate();

  const handleFormValidation = (e) => {
    e.preventDefault();
    // if (password1 !== password2) {
    //   setMessage("Passwords do not match");
    //   return;
    // }
    axios
      .post("http://localhost:8000/api/register/", {
        email: email,
        username: username,
        password1: password1,
        password2: password2,
      })
      .then((response) => {
        setMessage(response.data.message);
        navigate("/login");
      })
      .catch((error) => {
        console.log(error);
        setMessage("Error");
      });
  };

  return (
    <div className="register-content">
      <h1>Register</h1>
      <form className="register-form" onSubmit={handleFormValidation}>
        <label>Email</label>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <label>Username</label>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <label>Password</label>
        <input
          type="password"
          placeholder="Password"
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
        <label>Confirm password</label>
        <input
          type="password"
          placeholder="Confirm password"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
      {message && <p>{message}</p>}
      <Link to="/login">Login</Link>
    </div>
  );
};

export default Register;
