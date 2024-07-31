import React from "react";
import "./css/colors.css";
import "./css/index.css";
import { AuthProvider } from "./AuthContext";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Accueil from "./components/Accueil";
import NotFound from "./components/NotFound";
import PublicLayout from "./PublicLayout";
import PrivateLayout from "./PrivateLayout";
import Home from "./components/Home";
import Chat from "./components/Chat";
import Game from "./components/Game";
import UserSearch from "./components/UserSearch";
import Profile from "./components/Profile";
import Stats from "./components/Stats";
import ProfileEdit from "./components/ProfileEdit";
import ResetPassword from "./components/ResetPassword";
import ResetPasswordConfirm from "./components/ResetPasswordConfirm";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<PublicLayout />}>
            <Route path="/login" element={<Login />} />
            <Route path="/reset_password" element={<ResetPassword />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Accueil />} />
            <Route
              path="/reset/:uid/:token/"
              element={<ResetPasswordConfirm />}
            />
          </Route>

          <Route element={<PrivateLayout />}>
            <Route path="/home" element={<Home />} />
            <Route path="/chat/:cid?" element={<Chat />} />
            <Route path="/game/:invite?" element={<Game />} />
            <Route path="/search/:username" element={<UserSearch />} />
            <Route path="/profile/:id" element={<Profile />} />
            <Route path="/stats/:id" element={<Stats />} />
            <Route path="/profileedit" element={<ProfileEdit />} />
            <Route path="*" element={<NotFound />} />
          </Route>

          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
