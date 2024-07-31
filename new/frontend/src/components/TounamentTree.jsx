import React from "react";

const TounamentTree = ({ matchList }) => {
  return (
    <div className="cup-tree">
      {matchList &&
        matchList.map((round, index) => (
          <div className="cup-round" key={"round_" + index}>
            {round &&
              round.map((match, index) => (
                <div className="cup-match" key={"match_" + index}>
                  <div>{match.player1}</div>
                  <div>{match.player2}</div>
                </div>
              ))}
          </div>
        ))}
    </div>
  );
};

export default TounamentTree;
