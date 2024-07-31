import React from "react";

const ConvCard = ({ user, onClick, nonRead }) => {
  return (
    <div className="chat-user" onClick={onClick}>
      <img
        src={`http://localhost:8000${user.profile_picture}`}
        alt="profile picture"
      />
      <span>{user.username}</span>
      {nonRead && <div className="non-read"></div>}
      <div className="overlay"></div>
    </div>
  );
};

export default ConvCard;
