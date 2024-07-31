import React from "react";
import { Link } from "react-router-dom";

const Accueil = () => {
  return (
    <div>
      <h1>Accueil</h1>
      <Link to="/login">Login</Link>
      <Link to="/register">Register</Link>
    </div>
  );
};

export default Accueil;
