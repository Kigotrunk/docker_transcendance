import React from "react";

const PlayerCard = ({ player }) => {
  return (
    <div className="player-info">
      <img
        src={`http://localhost:8000${player.profile_picture}`}
        alt={`${player.username} profile picture`}
      />
      <span>{player.username}</span>
      <span>{player.elo}</span>
    </div>
  );
};

export default PlayerCard;
