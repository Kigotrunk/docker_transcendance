import React, { useState, useEffect, useRef, useContext } from "react";
import { AuthContext } from "../AuthContext";
import "../css/game.css";
import { useParams } from "react-router-dom";
import GameMenu from "./GameMenu";
import axios from "axios";
import TounamentTree from "./TounamentTree";
import PlayerCard from "./PlayerCard";

const PongGame = () => {
  const { invite } = useParams();
  const [lobbyState, setLobbyState] = useState("");
  const [gameStarted, setGameStarted] = useState(false);
  const [score, setScore] = useState("");
  const [countdown, setCountdown] = useState("");
  const [up, setUp] = useState(false);
  const [down, setDown] = useState(false);
  const canvasRef = useRef(null);
  const { gameSocketRef, gameSocketConnected, user } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(true);
  const [leftPlayer, setLeftPlayer] = useState(null);
  const [rightPlayer, setRightPlayer] = useState(null);
  const [matchList, setMatchList] = useState([]);
  const [menuState, setMenuState] = useState("");
  const [gameResult, setGameResult] = useState({});

  const handleSocketMessage = (e) => {
    const data = JSON.parse(e.data);
    if (!("type" in data)) {
      console.log(data);
      return;
    }
    if (data["type"] === "game_state") {
      setGameStarted(true);
      setMenuState("");
      updateGameState(data);
      return;
    }
    console.log(data);
    if (data["type"] === "status") {
      if (data["in_cup"]) {
        setMenuState("cup-waiting");
        setMatchList(data["matches"]);
      } else if (data["in_lobby"]) {
        setGameStarted(true);
      } else if (data["in_queue"]) {
        setMenuState("in-queue");
      } else if (data["in_queue_cup"]) {
        setMenuState("cup-queue");
      } else if (invite) {
        joinRoom("pvp", invite);
        setMenuState("waiting-opponent");
      } else {
        setMenuState("main");
      }
      setIsLoading(false);
    } else if (data["type"] === "lobby_state") {
      setLobbyState(data["message"]);
    } else if (data["type"] === "countdown") {
      setCountdown(data["countdown"]);
      setMenuState("countdown");
      if (data["countdown"] === "") {
        console.log("game: Game started");
        setGameStarted(true);
      }
    } else if (data["type"] === "tournament_state") {
      setMenuState("cup-waiting");
      setMatchList(data["matches"]);
    } else if (data["type"] === "game_info") {
      getPlayerProfile(data["left"], "left", data["left_username"]);
      getPlayerProfile(data["right"], "right", data["right_username"]);
    } else if (data["type"] === "game_result") {
      setGameResult(data["game_result"]);
      setMenuState("match-result");
    }
  };

  const getPlayerProfile = async (id, side, username) => {
    const response = await axios.get(
      `http://localhost:8000/api/profile/${id}/`
    );
    response.data["username"] = username;
    if (side === "left") {
      setLeftPlayer(response.data);
    }
    if (side === "right") {
      setRightPlayer(response.data);
    }
  };

  useEffect(() => {
    console.log("game: gameSocketRef.current", gameSocketRef.current);
    if (!gameSocketRef.current) {
      console.log("game: No game socket");
      setIsLoading(true);
      return;
    }
    gameSocketRef.current.addEventListener("message", handleSocketMessage);
    console.log("game: game socket event listener added");
    gameSocketRef.current.send(JSON.stringify({ action: "status" }));
    return () => {
      if (gameSocketRef.current) {
        gameSocketRef.current.removeEventListener(
          "message",
          handleSocketMessage
        );
      }
    };
  }, [gameSocketConnected]);

  const sendInput = (dir) => {
    if (!gameStarted || !gameSocketRef.current) {
      return;
    }
    gameSocketRef.current.send(
      JSON.stringify({ action: "move", direction: dir })
    );
  };

  useEffect(() => {
    sendInput(up - down);
  }, [up, down]);

  const handleKeyDown = (event) => {
    if (event.key === "ArrowUp" || event.key === "ArrowDown") {
      event.preventDefault();
    }
    if (gameStarted === false) {
      return;
    } //move menu ?
    if (event.key === "ArrowUp" && !up) {
      setUp(true);
    } else if (event.key === "ArrowDown" && !down) {
      setDown(true);
    }
  };

  const handleKeyUp = (event) => {
    if (event.key === "ArrowUp") {
      setUp(false);
    } else if (event.key === "ArrowDown") {
      setDown(false);
    }
  };

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("keyup", handleKeyUp);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("keyup", handleKeyUp);
    };
  }, [gameStarted]);

  const updateGameState = (gameState) => {
    const ctx = canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    ctx.fillStyle = "white";
    drawBall(ctx, gameState.ball_position);
    ctx.fillRect(0, gameState.paddle1_position, 10, 80);
    ctx.fillRect(790, gameState.paddle2_position, 10, 80);
    if ("score" in gameState) {
      setScore(`${gameState.score[0]} - ${gameState.score[1]}`);
    } else if ("surv_score" in gameState) {
      setScore(gameState["surv_score"]);
    }
    if ("game_over" in gameState && gameState["game_over"]) {
      setGameStarted(false);
      setLeftPlayer(null);
      setRightPlayer(null);
    }
  };

  const drawBall = (ctx, position) => {
    ctx.beginPath();
    ctx.arc(position[0], position[1], 10, 0, Math.PI * 2);
    ctx.fill();
  };

  const joinRoom = (mode, roomName) => {
    if (!gameSocketRef.current) return;

    gameSocketRef.current.send(
      JSON.stringify({
        action: "join",
        mode: mode,
        room: roomName,
      })
    );
  };

  useEffect(() => {
    const ctx = canvasRef.current.getContext("2d");
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    setScore("");
    if (menuState === "main") {
      setMatchList([]);
    }
  }, [menuState]);

  return (
    <div className="game-content">
      <div id="lobby-state">{lobbyState}</div>
      {isLoading && <div>Connection lost, trying to reconnect...</div>}
      <div id="game-info">
        {leftPlayer && <PlayerCard player={leftPlayer} />}
        <div id="game-container">
          <div id="score">{score}</div>
          <canvas
            id="pongCanvas"
            width="800"
            height="600"
            ref={canvasRef}
          ></canvas>
          <GameMenu
            menuState={menuState}
            setMenuState={setMenuState}
            joinRoom={joinRoom}
            countdown={countdown}
            gameResult={gameResult}
          />
        </div>
        {rightPlayer && <PlayerCard player={rightPlayer} />}
      </div>
      <TounamentTree matchList={matchList} />
    </div>
  );
};

export default PongGame;
