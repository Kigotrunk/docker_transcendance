import React, { useContext, useEffect } from "react";
import { Outlet, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Menu from "./components/Menu";
import { AuthContext } from "./AuthContext";

const PrivateLayout = () => {
  const { isLog, isLoading } = useContext(AuthContext);

  if (isLoading) {
    return <div>Loading...</div>;
  }
  return isLog ? (
    <>
      <Header />
      <div style={{ display: "flex", flexDirection: "row", flexGrow: 1 }}>
        <Menu />
        <div className="content" style={{ flexGrow: 1 }}>
          <Outlet />
        </div>
      </div>
    </>
  ) : (
    <Navigate to="/login" />
  );
};

export default PrivateLayout;
