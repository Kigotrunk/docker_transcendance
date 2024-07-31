import React, { useState } from "react";
import {
  MainMenu,
  VersusAiMenu,
  GameOverMenu,
  TournamentMenu,
  WaitingDuelMenu,
  GameResult,
} from "./GameMenuUtils";

const GameMenu = ({
  menuState,
  setMenuState,
  joinRoom,
  countdown,
  gameResult,
}) => {
  const getMenuState = () => {
    if (menuState === "") {
      return null;
    } else if (menuState === "main") {
      return <MainMenu joinRoom={joinRoom} setMenuState={setMenuState} />;
    } else if (menuState === "ai") {
      return <VersusAiMenu joinRoom={joinRoom} setMenuState={setMenuState} />;
    } else if (menuState === "tournament") {
      return <TournamentMenu joinRoom={joinRoom} setMenuState={setMenuState} />;
    } else if (menuState === "duel") {
      return (
        <WaitingDuelMenu joinRoom={joinRoom} setMenuState={setMenuState} />
      );
    } else if (menuState === "cup-waiting") {
      return <div>Waiting for the next match</div>;
    } else if (menuState === "countdown") {
      return <div style={{ fontSize: "64px" }}>{countdown}</div>;
    } else if (menuState === "game-over") {
      return <GameOverMenu joinRoom={joinRoom} setMenuState={setMenuState} />;
    } else if (menuState === "cup-loser") {
      return <div>You lost the cup</div>;
    } else if (menuState === "cup-winner") {
      return <div>Congratulations! You won the cup</div>;
    } else if (menuState === "match-result") {
      return <GameResult gameResult={gameResult} setMenuState={setMenuState} />;
    } else if (menuState === "waiting-opponent") {
      return <div>Waiting for opponent...</div>;
    }
    return null;
  };

  return <div className="game-menu">{getMenuState()}</div>;
};

export default GameMenu;
