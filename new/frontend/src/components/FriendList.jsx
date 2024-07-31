import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/friendlist.css";
import { Link } from "react-router-dom";

const FriendList = () => {
  const [friendList, setFriendList] = useState([]);

  useEffect(() => {
    getFriendList();
  }, []);

  const getFriendList = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/friend_list/`);
      console.log(response.data);
      const connected = response.data
        .filter((friend) => friend.is_connected)
        .sort((a, b) => a.username.localeCompare(b.username));
      const disconnected = response.data
        .filter((firend) => !firend.is_connected)
        .sort((a, b) => a.username.localeCompare(b.username));
      const sortedUsers = [...connected, ...disconnected];
      setFriendList(sortedUsers);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="friend-list">
      {friendList.map((friend) => (
        <Link to={`/profile/${friend.id}`} key={friend.id} className="friend">
          <img
            src={`http://localhost:8000${friend.profile_picture}`}
            alt={`${friend.username}'s profile picture`}
            className={`${friend.is_connected ? "connected" : "disconnected"}`}
          />
          <span>{friend.username}</span>
        </Link>
      ))}
    </div>
  );
};

export default FriendList;
