import React, { useContext } from "react";
import { AuthContext } from "../../AuthContext";

const GameResult = ({ gameResult, setMenuState }) => {
  const { user } = useContext(AuthContext);
  if (gameResult["mode"] === "ia") {
    return (
      <div className="game-result">
        <h2>Game Over</h2>
        <span>{gameResult["win"] ? "You win" : "You lose"}</span>
      </div>
    );
  }

  return (
    <div className="game-result">
      {gameResult["winner"] == user.id ? "You win" : "You lose"}
      {gameResult["mode"] === "cup" && gameResult["winner"] == user.id ? (
        "You advance to the next round"
      ) : (
        <button onClick={() => setMenuState("main")}>Back to main menu</button>
      )}
    </div>
  );
};

export default GameResult;
