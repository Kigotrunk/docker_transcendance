import React from "react";

const MainMenu = ({ joinRoom, setMenuState }) => {
  return (
    <div id="game-main-menu">
      <button onClick={() => setMenuState("duel")}>Duel</button>
      <button onClick={() => setMenuState("tournament")}>Tournament</button>
      <button onClick={() => setMenuState("ai")}>Play AI</button>
    </div>
  );
};

export default MainMenu;
