import React, { useEffect, useState } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import ConversationList from "../components/ConversationList";

const Conversations = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState("Tous");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/conversations")
      .then((response) => setConversations(response.data))
      .catch((error) => console.error("Erreur API :", error));
  }, []);

  return (
    <div className="conversation-layout">
      {/* Sidebar en haut, fixe */}
      <Sidebar selectedFolder={selectedFolder} setSelectedFolder={setSelectedFolder} />

      {/* Liste des conversations, mobile avec scroll */}
      <div className="conversation-list-container">
        <ConversationList conversations={conversations} selectedFolder={selectedFolder} />
      </div>
    </div>
  );
};

export default Conversations;
