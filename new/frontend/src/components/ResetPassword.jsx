import React, { useContext, useState } from "react";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

const ResetPassword = () => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleReset = async (event) => {
    event.preventDefault();
    setError("");
    try {
      const response = await axios.post(
        "http://localhost:8000/api/reset_password/",
        {
          email: email,
        }
      );
    } catch (err) {
      console.error(err);
      setError("Invalid Credentials");
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <form onSubmit={handleReset}>
        <div>
          <label>Email:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <button type="submit">Send Email</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default ResetPassword;
