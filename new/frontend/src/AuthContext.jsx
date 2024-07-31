import { createContext, useEffect, useState, useRef } from "react";
import axios from "axios";
import { set } from "lodash";

const AuthContext = createContext();

function AuthProvider(props) {
  const [isLog, setIsLog] = useState(false);
  const [access, setAccess] = useState("");
  const [refresh, setRefresh] = useState(localStorage.getItem("refresh") || "");
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const chatSocketRef = useRef(null);
  const gameSocketRef = useRef(null);
  const [chatNotifsId, setChatNotifsId] = useState([]);
  const [gameSocketConnected, setGameSocketConnected] = useState(false);
  const [chatSocketConnected, setChatSocketConnected] = useState(false);
  const [currentGameMode, setCurrentGameMode] = useState("");

  const setTokens = (access, refresh) => {
    setAccess(access);
    setRefresh(refresh);
    localStorage.setItem("refresh", refresh);
  };

  const removeTokens = () => {
    setAccess("");
    setRefresh("");
    localStorage.removeItem("refresh");
  };

  const login = (user, access, refresh) => {
    console.log(access, refresh);
    setTokens(access, refresh);
    setUser(user);
    axios.defaults.headers.common["Authorization"] = `Bearer ${access}`;
    openChatSocket(access);
    openGameSocket(access);
    setIsLog(true);
    setIsLoading(false);
  };

  const logout = () => {
    removeTokens();
    setUser(null);
    axios.defaults.headers.common["Authorization"] = null;
    if (chatSocketRef.current) {
      chatSocketRef.current.close();
      chatSocketRef.current = null;
    }
    if (gameSocketRef.current) {
      gameSocketRef.current.close();
      gameSocketRef.current = null;
    }
    setIsLog(false);
    setIsLoading(false);
  };

  const refreshUser = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/api/profile/${user.id}/`
      );
      console.log(response.data);
      setUser(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const updateAccess = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/refresh/", {
        refresh: refresh,
      });
      if (response.status === 200) {
        console.log("access", response.data.access);
        setAccess(response.data.access);
        setUser(response.data.user);
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${response.data.access}`;
        openChatSocket(response.data.access);
        openGameSocket(response.data.access);
        setIsLog(true);
      } else {
        logout();
      }
    } catch (error) {
      console.error(error);
      logout();
    } finally {
      setIsLoading(false);
    }
  };

  const openChatSocket = (newAccess) => {
    if (chatSocketRef.current) {
      return;
    }

    const socket = new WebSocket(
      `ws://localhost:8000/ws/chat/?token=${newAccess}`
    );

    socket.onopen = () => {
      console.log("ChatSocket connection opened");
      chatSocketRef.current = socket;
      setChatSocketConnected(true);
    };

    socket.onerror = (e) => {
      console.error("ChatSocket error", e);
    };

    socket.onclose = (e) => {
      console.log("ChatSocket closed", e);
      chatSocketRef.current = null;
      setChatSocketConnected(false);
    };
  };

  const openGameSocket = (newAccess) => {
    if (gameSocketRef.current) {
      return;
    }

    const socket = new WebSocket(
      `ws://localhost:8000/ws/pong/?token=${newAccess}`
    );

    socket.onopen = () => {
      console.log("GameSocket connection opened");
      gameSocketRef.current = socket;
      setGameSocketConnected(true);
    };

    socket.onerror = (e) => {
      console.error("GameSocket error", e);
    };

    socket.onclose = (e) => {
      console.log("GameSocket closed", e);
      gameSocketRef.current = null;
      setGameSocketConnected(false);
    };
  };

  useEffect(() => {
    if (refresh) {
      updateAccess();
    } else {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (refresh) {
      const interval = setInterval(updateAccess, 290000);
      return () => clearInterval(interval);
    }
  }, [refresh]);

  const value = {
    isLog,
    user,
    access,
    login,
    logout,
    isLoading,
    chatSocketRef,
    gameSocketRef,
    chatNotifsId,
    setChatNotifsId,
    refreshUser,
    gameSocketConnected,
    chatSocketConnected,
  };

  return <AuthContext.Provider value={value} {...props} />;
}

export { AuthContext, AuthProvider };
