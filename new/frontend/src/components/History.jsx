import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import "../css/history.css";

const History = ({ id }) => {
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(1);
  const [showMore, setShowMore] = useState(true);

  useEffect(() => {
    getHistory();
  }, [id]);

  const getHistory = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/game/history/${id}/?page=1`
      );
      setHistory(response.data.results);
    } catch (error) {
      console.error(error);
    }
  };

  const SeeMore = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/game/history/${id}/?page=${page + 1}`
      );
      setHistory((prevHistory) => [...prevHistory, ...response.data.results]);
      setPage(page + 1);
    } catch (error) {
      console.log("no more games");
      setShowMore(false);
    }
  };

  const Match = ({ game }) => {
    let result =
      game.player1.id == id
        ? game.score_player1 - game.score_player2
        : game.score_player2 - game.score_player1;
    return (
      <div className={`match ${result > 0 ? "win" : result < 0 ? "lose" : ""}`}>
        <Link to={`/profile/${game.player1.id}`} className="history-user">
          {game.player1.username}
        </Link>
        <div className="history-score">
          {game.score_player1} - {game.score_player2}
        </div>
        <Link to={`/profile/${game.player2.id}`} className="history-user">
          {game.player2.username}
        </Link>
        <div className="history-time">
          {new Date(game.time).toLocaleDateString()}
        </div>
      </div>
    );
  };

  if (history.length === 0) {
    return <div className="history">No games played yet</div>;
  }

  return (
    <div className="history">
      <div>
        In the last {history.length} games:{" "}
        {
          history.filter((game) => game.score_player1 > game.score_player2)
            .length
        }{" "}
        wins,{" "}
        {
          history.filter((game) => game.score_player1 < game.score_player2)
            .length
        }{" "}
        defeats
      </div>
      {history.map((game, index) => (
        <Match key={index} game={game} />
      ))}
      {showMore && (
        <div className="history-see-more" onClick={SeeMore}>
          See More
        </div>
      )}
    </div>
  );
};

export default History;
