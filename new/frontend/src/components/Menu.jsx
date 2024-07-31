import React, { useEffect, useContext, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import "../css/menu.css";
import SportsEsportsIcon from "@mui/icons-material/SportsEsports";
import ChatIcon from "@mui/icons-material/Chat";
import TimelineIcon from "@mui/icons-material/Timeline";
import LogoutIcon from "@mui/icons-material/Logout";
import { AuthContext } from "../AuthContext";

const Menu = () => {
  const { logout, user, chatSocketRef, chatNotifsId, setChatNotifsId } =
    useContext(AuthContext);
  const [gameNotifs, setGameNotifs] = useState(false);

  const addChatNotif = (e) => {
    const data = JSON.parse(e.data);
    if (data.issuer === user.username) return;
    console.log(data);
    if (data.issuer === "Tournament Info") {
      if (window.location.pathname !== "/game") setGameNotifs(true);
      return;
    }
    setChatNotifsId((prev) => {
      if (prev.includes(data.conversation_id)) return prev;
      return [...prev, data.conversation_id];
    });
  };

  useEffect(() => {
    if (!chatSocketRef.current) {
      console.log("menu: No chat socket");
      return;
    }
    console.log("menu: Adding chat notif listener");
    chatSocketRef.current.addEventListener("message", addChatNotif);
    return () => {
      if (chatSocketRef.current) {
        chatSocketRef.current.removeEventListener("message", addChatNotif);
      }
    };
  }, [chatSocketRef.current]);

  return (
    <>
      <div className="phone-menu">
        <div
          style={{ width: "100%", height: "80px", backgroundColor: "black" }}
        ></div>
        <NavLink to="/game">
          <span>Game</span>
        </NavLink>
        <NavLink to="/chat">
          <span>Chat</span>
        </NavLink>
        <Link onClick={logout}>
          <span>Logout</span>
        </Link>
      </div>

      <div className="blured"></div>

      <div className="menu">
        <NavLink to="/game" onClick={() => setGameNotifs(false)}>
          <SportsEsportsIcon fontSize="inherit"></SportsEsportsIcon>
          {gameNotifs && <div className="notif">!</div>}
        </NavLink>

        <NavLink to="/chat">
          <ChatIcon fontSize="inherit"></ChatIcon>
          {chatNotifsId.length > 0 && (
            <div className="notif">{chatNotifsId.length}</div>
          )}
        </NavLink>

        <NavLink to={`/stats/${user.id}`}>
          <TimelineIcon fontSize="inherit"></TimelineIcon>
        </NavLink>

        <Link onClick={logout} style={{ marginTop: "auto" }}>
          <LogoutIcon fontSize="inherit"></LogoutIcon>
        </Link>
      </div>
    </>
  );
};

export default Menu;
