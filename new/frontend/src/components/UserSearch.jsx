import React, { useEffect, useState, useContext } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";
import "../css/usersearch.css";

const UserSearch = () => {
  const { username } = useParams();
  const [userList, setUserList] = useState([]);

  const searchUsers = async () => {
    const response = await axios.get(
      `http://localhost:8000/api/users/?search=${username}`
    );
    setUserList(response.data);
  };

  useEffect(() => {
    searchUsers();
  }, [username]);

  if (userList.length === 0) {
    return <div className="message">No user found</div>;
  }

  return (
    <div className="user-search">
      {userList.map((user) => (
        <Link to={`/profile/${user.id}`} key={user.id} className="user-found">
          <img src={`http://localhost:8000${user.profile_picture}`}></img>
          <span>{user.username}</span>
        </Link>
      ))}
    </div>
  );
};

export default UserSearch;
