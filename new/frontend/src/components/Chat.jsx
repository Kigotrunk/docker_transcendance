import React, { useState, useEffect, useContext, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "../css/chat.css";
import { AuthContext } from "../AuthContext";
import axios from "axios";
import ConvCard from "./ChatUtils/ConvCard";
import ChatHeader from "./ChatUtils/ChatHeader";
import NewConv from "./ChatUtils/NewConv";
import TalkSection from "./ChatUtils/TalkSection";

const Chat = () => {
  const { cid } = useParams();
  const navigate = useNavigate();
  const [conversations, setConversations] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [isBlocked, setIsBlocked] = useState(false);
  const [newConv, setNewConv] = useState(false);
  const { user, setChatNotifsId, chatNotifsId, chatSocketRef } =
    useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(true);

  const getConversations = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/api/conversations/?page=1`
      );
      const modifiedConversations = response.data.results.map(
        (conversation) => {
          return {
            ...conversation,
            user:
              conversation.user1.id !== user.id
                ? conversation.user1
                : conversation.user2,
          };
        }
      );
      setConversations(modifiedConversations);
      if (cid) {
        setSelectedChat(modifiedConversations.find((conv) => conv.id == cid));
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (!chatSocketRef.current) {
      setIsLoading(true);
      return;
    }
    chatSocketRef.current.addEventListener("message", getConversations);
    setIsLoading(false);
    return () => {
      if (chatSocketRef.current) {
        chatSocketRef.current.removeEventListener("message", getConversations);
      }
    };
  }, [chatSocketRef.current]);

  useEffect(() => {
    getConversations();
  }, []);

  const getBlockedStatus = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/block_status/?other_id=${selectedChat.user.id}`
      );
      setIsBlocked(response.data.blocked);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    if (conversations.length > 0) {
      setSelectedChat(conversations.find((conv) => conv.id == cid));
    }
  }, [cid]);

  useEffect(() => {
    if (selectedChat) {
      getBlockedStatus();
    }
  }, [selectedChat]);

  return (
    <div className="chat-content">
      <div className="conv-list">
        <div className="conv-header">
          <span>Privates messages</span>
          <div
            id="new-conv-btn"
            title="New private message"
            onClick={() => setNewConv(true)}
          >
            +
          </div>
        </div>
        {conversations.map((conversation) => (
          <ConvCard
            key={conversation.id}
            onClick={() => {
              navigate(`/chat/${conversation.id}`);
              setChatNotifsId((prev) =>
                prev.filter((id) => id !== conversation.id)
              );
            }}
            user={conversation.user}
            nonRead={chatNotifsId.includes(conversation.id)}
          />
        ))}
      </div>
      {!isLoading && selectedChat && (
        <div className="chat-right-section">
          <ChatHeader
            user2={selectedChat.user}
            isBlocked={isBlocked}
            setIsBlocked={setIsBlocked}
          />
          <TalkSection
            cid={selectedChat.id}
            user2={selectedChat.user}
            isBlocked={isBlocked}
            getConversations={getConversations}
          />
        </div>
      )}
      {newConv ? (
        <NewConv setNewConv={setNewConv} getConversations={getConversations} />
      ) : null}
    </div>
  );
};

export default Chat;
