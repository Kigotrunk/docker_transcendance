import React, { useContext, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import BlockIcon from "@mui/icons-material/Block";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import GamepadIcon from "@mui/icons-material/Gamepad";
import CancelIcon from "@mui/icons-material/Cancel";
import axios from "axios";
import { AuthContext } from "../../AuthContext";
import { set } from "lodash";

const ChatHeader = ({ user2, isBlocked, setIsBlocked }) => {
  const [showAddButton, setShowAddButton] = useState(false);
  const [friendStatus, setFriendStatus] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState(false);
  const { user, chatSocketRef } = useContext(AuthContext);
  const navigate = useNavigate();

  const getFriendStatus = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/friend_status/?friend_id=${user2.id}`
      );
      if (response.data.friendStatus === "none") {
        setShowAddButton(true);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const getConnectionStatus = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/connection_status/${user2.id}/`
      );
      console.log(response.data);
      setFriendStatus(response.data.is_friend);
      setConnectionStatus(response.data.is_connected);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    getFriendStatus();
    getConnectionStatus();
  }, [user2]);

  const addFriend = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/send_invitation/?receiver_id=${user2.id}`
      );
      console.log(response.data);
      setShowAddButton(false);
    } catch (error) {
      console.error(error);
    }
  };

  const inviteInGame = () => {
    const gameId = `${user.id}-${user2.id}`;
    chatSocketRef.current.send(
      JSON.stringify({
        message: `/invite ${gameId}`,
        issuer: user.username,
        receiver: user2.username,
      })
    );
    navigate(`/game/${gameId}`);
  };

  const blockUser = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/block_user/?blocked_id=${user2.id}`
      );
      console.log(response.data);
      setIsBlocked(true);
    } catch (error) {
      console.error(error);
    }
  };

  const unblockUser = async () => {
    try {
      const response = await axios.post(
        `http://localhost:8000/block_user/?blocked_id=${user2.id}&unblock=true`
      );
      console.log(response.data);
      setIsBlocked(false);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="chat-header">
      <div className="chat-header-user">
        <Link to={`/profile/${user2.id}`}>
          <div className="chat-header-pic">
            <img
              src={`http://localhost:8000${user2.profile_picture}`}
              alt="profile picture"
            />
            {friendStatus &&
              (connectionStatus ? (
                <div className="online-led"></div>
              ) : (
                <div className="offline-led"></div>
              ))}
          </div>
          <span>{user2.username}</span>
        </Link>
        {showAddButton && (
          <div
            className="btn btn-primary"
            title="Add friend"
            onClick={addFriend}
          >
            <PersonAddIcon fontSize="small" />
          </div>
        )}
      </div>
      <div className="chat-header-actions">
        <div
          className="btn btn-primary"
          title="Invite in game"
          onClick={inviteInGame}
        >
          <GamepadIcon fontSize="small" />
          <span>Invite in game</span>
        </div>
        {isBlocked ? (
          <div className="btn" title="Unblock user" onClick={unblockUser}>
            <CancelIcon fontSize="small" />
          </div>
        ) : (
          <div className="btn" title="Block user" onClick={blockUser}>
            <BlockIcon fontSize="small" />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatHeader;
