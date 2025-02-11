import React from "react";
import { Link } from "react-router-dom";

const ConversationItem = ({ conversation }) => {
  return (
    <div className="conversation-card">
      <Link to={`/conversation/${conversation.id}`} className="conversation-title">
        {conversation.title}
      </Link>
      <div className="conversation-meta">
        <span className="meta-item">📅 {new Date(conversation.create_time * 1000).toLocaleDateString()}</span>
        <span className="meta-item">🤖 {conversation.model}</span>
      </div>
      <div className="conversation-actions">
        <button className="archive-button">📂 Archiver</button>
        <button className="edit-button">✏️ Modifier</button>
      </div>
    </div>
  );
};

export default ConversationItem;
