import React, { useContext, useRef, useState, useEffect } from "react";
import SendIcon from "@mui/icons-material/Send";
import { AuthContext } from "../../AuthContext";
import axios from "axios";
import { debounce, get, set } from "lodash";
import { Link } from "react-router-dom";

const TalkSection = ({ cid, user2, isBlocked, getConversations }) => {
  const talkDiv = useRef(null);
  const [messageInput, setMessageInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [page, setPage] = useState(1);
  const { user, chatSocketRef, setChatNotifsId } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  const handleSocketMessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data);
    getConversations();
    if (data.conversation_id != cid) {
      return;
    }
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        message: data.message,
        issuer: { username: data.issuer },
      },
    ]);
    resetScroll();
  };

  useEffect(() => {
    if (!chatSocketRef.current) {
      setLoading(true);
      return;
    }
    setLoading(false);
    chatSocketRef.current.addEventListener("message", handleSocketMessage);
    return () => {
      if (chatSocketRef.current) {
        chatSocketRef.current.removeEventListener(
          "message",
          handleSocketMessage
        );
      }
    };
  }, [cid, chatSocketRef.current]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!cid || messageInput.trim() === "") {
      return;
    }

    try {
      chatSocketRef.current.send(
        JSON.stringify({
          message: messageInput,
          issuer: user.username,
          receiver: user2.username,
        })
      );
      setMessageInput("");
      resetScroll();
    } catch (error) {
      console.error(error);
    }
  };

  const getMessages = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/conversations/${cid}/?page=1`
      );
      setMessages(response.data.results.toReversed());
    } catch (error) {
      console.error(error);
    }
  };

  const getMoreMessages = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/conversations/${cid}/?page=${page}`
      );
      setMessages((prevMessages) => [
        ...response.data.results.toReversed(),
        ...prevMessages,
      ]);
    } catch (error) {
      console.log("no more messages");
    }
  };

  useEffect(() => {
    if (isBlocked) {
      return;
    }
    getMessages();
    setPage(1);
    if (talkDiv.current) {
      talkDiv.current.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (talkDiv.current) {
        talkDiv.current.removeEventListener("scroll", handleScroll);
      }
    };
  }, [cid, isBlocked]);

  useEffect(() => {
    if (page > 1) {
      getMoreMessages();
    }
  }, [page]);

  const handleScroll = debounce(() => {
    if (
      talkDiv.current &&
      talkDiv.current.scrollTop +
        talkDiv.current.scrollHeight -
        talkDiv.current.offsetHeight <
        100
    ) {
      setPage((prevPage) => prevPage + 1);
    }
    if (talkDiv.current.scrollTop > -5) {
      console.log("removing notif");
      setChatNotifsId((prev) => prev.filter((id) => id != cid));
    }
  }, 100);

  const resetScroll = () => {
    if (talkDiv.current) {
      talkDiv.current.scrollTop = 0;
    }
  };

  if (loading) {
    return (
      <div className="loading">Connection lost, trying to reconnect...</div>
    );
  }

  if (isBlocked) {
    return <div className="loading">You have blocked this user</div>;
  }

  return (
    <>
      <div className="talk" ref={talkDiv}>
        {messages.map((message, index) =>
          message.message.startsWith("/invite ") ? (
            <div
              key={index}
              className={`invite ${
                message.issuer.username === user.username ? "sent" : "received"
              }`}
            >
              <span>{message.issuer.username} wants to play !</span>
              <Link to={`/game/${message.message.split(" ")[1]}`}>Join</Link>
            </div>
          ) : (
            <div
              key={index}
              className={`chat-message ${
                message.issuer.username === user.username ? "sent" : "received"
              }`}
            >
              {message.message}
            </div>
          )
        )}
      </div>

      <form onSubmit={sendMessage} className="message-form">
        <div className="input">
          <input
            type="text"
            className="text-input"
            placeholder="Type a message"
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            autoComplete="off"
            required
          />
          <button
            type="submit"
            className="send-button"
            disabled={messageInput.trim() === ""}
          >
            <SendIcon fontSize="small"></SendIcon>
          </button>
        </div>
      </form>
    </>
  );
};

export default TalkSection;
