import React, { useState, useContext, useEffect } from "react";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { AuthContext } from "../../AuthContext";

const TournamentMenu = ({ joinRoom, setMenuState }) => {
  const [inQueue, setInQueue] = useState(false);
  const { gameSocketRef } = useContext(AuthContext);

  const leaveQueue = () => {
    console.log("Leaving cup");
    if (
      gameSocketRef.current &&
      gameSocketRef.current.readyState === WebSocket.OPEN
    ) {
      gameSocketRef.current.send(
        JSON.stringify({
          action: "leave_cup",
        })
      );
      console.log("Sent leave cup message");
      setInQueue(false);
    } else {
      console.error("WebSocket is not open or not initialized");
    }
  };
  /*
  useEffect(() => {
    return () => {
      if (inQueue) {
        leaveQueue();
      }
    };
  }, [inQueue]);
*/

  return (
    <div className="cup-menu">
      <h2>Tournament</h2>
      {inQueue ? (
        <div className="menu-queue-state">
          <span>Waiting for more players...</span>
          <div className="loader"></div>
          <div className="cancel-btn" onClick={leaveQueue}>
            Cancel
          </div>
        </div>
      ) : (
        <div
          className="join-btn"
          onClick={() => {
            joinRoom("pvp", "cup");
            setInQueue(true);
          }}
        >
          Join
        </div>
      )}
      <button
        className="btn-back"
        onClick={() => {
          setMenuState("main");
        }}
      >
        <ArrowBackIcon fontSize="large" />
      </button>
    </div>
  );
};

export default TournamentMenu;
