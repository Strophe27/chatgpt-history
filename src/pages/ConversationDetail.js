import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

const ConversationDetail = () => {
  const { id } = useParams();
  const [conversation, setConversation] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/conversation/${id}`)
      .then((response) => setConversation(response.data))
      .catch((error) => console.error("Erreur API :", error));
  }, [id]);

  if (!conversation) {
    return <div className="conversation-detail">Chargement...</div>;
  }

  return (
    <div className="conversation-detail">
      <h1>{conversation.title}</h1>
      <p><strong>📅 Date :</strong> {new Date(conversation.create_time * 1000).toLocaleDateString()}</p>
      <p><strong>🤖 Modèle :</strong> {conversation.model}</p>
      <p><strong>📂 Agent :</strong> {conversation.agent_name || "Inconnu"}</p>
      <pre className="conversation-content">{conversation.content || "🚨 Aucun contenu disponible."}</pre>
      <Link to="/" className="back-button">🔙 Retour</Link>
    </div>
  );
};

export default ConversationDetail;
