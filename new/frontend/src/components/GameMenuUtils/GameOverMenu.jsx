import React from "react";

const GameOverMenu = ({ joinRoom, setMenuState }) => {
  return (
    <div id="game-over">
      <span>GAME OVER</span>
      <div>
        <button className="secondary-btn" onClick={() => setMenuState("main")}>
          Return Menu
        </button>
      </div>
    </div>
  );
};

export default GameOverMenu;
