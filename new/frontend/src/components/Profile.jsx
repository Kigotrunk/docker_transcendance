import React, { useEffect, useState, useContext } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import History from "./History";
import "../css/profile.css";
import ProfileActions from "./ProfileUtils.jsx/ProfileActions";
import { set } from "lodash";

const Profile = () => {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState(false);
  const [inGame, setInGame] = useState(false);
  const navigate = useNavigate();

  const isMyProfile = id == user.id;

  const getProfile = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/profile/${id}/`
      );
      console.log(response.data);
      setProfile(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getConnectionStatus = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/connection_status/${id}/`
      );
      console.log(response.data);
      setConnectionStatus(response.data.is_connected);
      setInGame(response.data.is_in_game);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    window.scrollTo(0, 0);
    getProfile();
    getConnectionStatus();
  }, [id]);

  if (!profile) {
    return <div>Loading...</div>;
  }

  return (
    <div className="profile-content">
      <div className="profile-card">
        <div className="profile-picture">
          {isMyProfile && (
            <div className="img-hover" onClick={() => navigate("/profileedit")}>
              <span className="material-icons">edit</span>
            </div>
          )}
          <img
            src={`http://localhost:8000${profile.profile_picture}`}
            alt="profile picture"
          />
        </div>
        <div className="profile-info">
          <div className="profile-upper-line">
            <span>{profile.username}</span>
            {isMyProfile ? (
              <Link className="btn-grey" to="/profileedit">
                Edit Profile
              </Link>
            ) : (
              <ProfileActions user2={profile} />
            )}
          </div>
          <div>
            <p>
              {profile.nb_win} Wins - {profile.nb_top1} Cup Wins - {profile.elo}{" "}
              LP
            </p>
            {inGame ? <p>In Game</p> : connectionStatus && <p>Online</p>}
          </div>
        </div>
      </div>
      <div className="divider"></div>
      <History id={profile.id} />
    </div>
  );
};

export default Profile;
