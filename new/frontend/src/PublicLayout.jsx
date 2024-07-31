import React, { useContext, useEffect } from "react";
import { Outlet, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Menu from "./components/Menu";
import { AuthContext } from "./AuthContext";

const PublicLayout = () => {
  const { isLog, isLoading } = useContext(AuthContext);

  if (isLoading) {
    return <div>Loading...</div>;
  }
  return !isLog ? <Outlet /> : <Navigate to="/home" />;
};

export default PublicLayout;
