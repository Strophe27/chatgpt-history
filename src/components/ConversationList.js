import React from "react";
import ConversationItem from "./ConversationItem";

const ConversationList = ({ conversations, selectedFolder }) => {
  // ✅ Ajout d'une vérification pour éviter les erreurs
  if (!conversations || conversations.length === 0) {
    return <p>🔍 Aucune conversation trouvée.</p>;
  }

  // ✅ Ajout d'une vérification sur chaque conversation pour éviter les erreurs
  const filteredConversations = conversations.filter((conv) => {
    return (
      conv && // Vérifie que conv n'est pas undefined
      (selectedFolder === "Tous" || conv.folder === selectedFolder) && // Filtrage par dossier
      (conv.gizmo_id || "Inconnu") // S'assure que gizmo_id est bien défini
    );
  });

  return (
    <div className="conversation-list">
      {filteredConversations.length > 0 ? (
        filteredConversations.map((conv) => (
          <ConversationItem key={conv.id} conversation={conv} />
        ))
      ) : (
        <p>🔍 Aucune conversation correspondante.</p>
      )}
    </div>
  );
};

export default ConversationList;
