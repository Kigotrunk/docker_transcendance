import React, { useContext, useState, useEffect } from "react";
import { AuthContext } from "../../AuthContext";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const WaitingDuelMenu = ({ joinRoom, setMenuState }) => {
  const [inQueue, setInQueue] = useState(false);
  const { gameSocketRef } = useContext(AuthContext);
  const leaveQueue = () => {
    console.log("Leaving queue");
    if (
      gameSocketRef.current &&
      gameSocketRef.current.readyState === WebSocket.OPEN
    ) {
      gameSocketRef.current.send(
        JSON.stringify({
          action: "leave_queue",
        })
      );
      console.log("Sent leave queue message");
      setInQueue(false);
    } else {
      console.error("WebSocket is not open or not initialized");
    }
  };

  useEffect(() => {
    return () => {
      if (inQueue) {
        leaveQueue();
      }
    };
  }, [inQueue]);

  return (
    <div className="cup-menu">
      <h2>Duel</h2>
      {inQueue ? (
        <div className="menu-queue-state">
          <span>Waiting for opponent...</span>
          <div className="loader"></div>
          <div className="cancel-btn" onClick={leaveQueue}>
            Cancel
          </div>
        </div>
      ) : (
        <div
          className="join-btn"
          onClick={() => {
            joinRoom("pvp", "matchmaking");
            setInQueue(true);
          }}
        >
          Find a game
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

export default WaitingDuelMenu;
