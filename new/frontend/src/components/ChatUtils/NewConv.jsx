import React, { useState, useContext } from "react";
import { AuthContext } from "../../AuthContext";

const NewConv = ({ setNewConv, getConversations }) => {
  const [newUser, setNewUser] = useState("");
  const [messageInput, setMessageInput] = useState("");
  const [error, setError] = useState("");
  const { user, chatSocketRef } = useContext(AuthContext);

  const createConv = (e) => {
    e.preventDefault();
    if (messageInput.trim() === "") {
      setError("Message cannot be empty");
      return;
    }
    chatSocketRef.current.send(
      JSON.stringify({
        type: "message",
        issuer: user.username,
        receiver: newUser,
        message: messageInput,
      })
    );
    getConversations();
    setNewConv(false);
  };

  const handleClickOutside = () => {
    setNewConv(false);
  };

  const handleClickForm = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="backdrop" onClick={handleClickOutside}>
      <form
        onSubmit={createConv}
        className="new-conv-form"
        onClick={handleClickForm}
      >
        <input
          type="text"
          placeholder="Username"
          value={newUser}
          onChange={(e) => setNewUser(e.target.value)}
        />
        <input
          type="text"
          placeholder="Message"
          value={messageInput}
          onChange={(e) => setMessageInput(e.target.value)}
        />
        <button type="submit">Send</button>
        <p>{error}</p>
      </form>
    </div>
  );
};

export default NewConv;
