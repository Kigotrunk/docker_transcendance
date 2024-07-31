import React from "react";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const VersusAiMenu = ({ joinRoom, setMenuState }) => {
  const levels = ["Easy", "Medium", "Hard", "Survival"];
  return (
    <div className="game-menu">
      {levels.map((level, index) => (
        <button key={index} onClick={() => joinRoom("ai", index + 1)}>
          {level}
        </button>
      ))}
      <button className="btn-back" onClick={() => setMenuState("main")}>
        <ArrowBackIcon fontSize="large" />
      </button>
    </div>
  );
};

export default VersusAiMenu;
