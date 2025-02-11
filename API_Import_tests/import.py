import ijson

# Chemin du fichier JSON
json_file = "conversations.json"
target_index = 127  # Numéro de la conversation à extraire

# Dictionnaire des gizmo_id connus
gizmo_mapping = {
    "g-rBaxjvzwq": "Mon Irma",
    # Ajoute d'autres gizmo_id ici au fur et à mesure...
}

# Lecture en streaming
with open(json_file, "rb") as f:
    parser = ijson.items(f, "item")
    
    conversation = None
    for index, conv in enumerate(parser, start=1):
        if index == target_index:
            conversation = conv
            break  # Arrêter dès qu'on a trouvé la bonne conversation

# Vérification si la conversation existe
if not conversation:
    print(f"Aucune conversation trouvée à l'index {target_index}.")
    exit()

# Extraction des infos principales
title = conversation.get("title", "Sans titre")
create_time = conversation.get("create_time", "Inconnu")
mapping = conversation.get("mapping", {})

# Détection du modèle utilisé et de l'archivage
default_model_slug = conversation.get("default_model_slug", "Inconnu")
is_archived = conversation.get("is_archived", False)  # `False` si absent

# Identification de l'agent (gizmo)
gizmo_id = conversation.get("gizmo_id", "Inconnu")
agent_name = gizmo_mapping.get(gizmo_id, gizmo_id)  # Utilisation du mapping si disponible

# Récupération des messages en suivant `current_node`
current_node = conversation.get("current_node")
messages = []

while current_node:
    node = mapping.get(current_node)
    if not node:
        break  

    message_data = node.get("message")
    if message_data:
        author_role = message_data.get("author", {}).get("role", "inconnu")
        message_time = message_data.get("create_time", "Inconnu")  # Récupérer le timestamp
        content_obj = message_data.get("content", {})
        parts = content_obj.get("parts", [])

        text_parts = []
        is_transcript = False

        for part in parts:
            if isinstance(part, str) and part.strip():
                text_parts.append(part.strip())
            elif isinstance(part, dict) and part.get("content_type") == "audio_transcription":
                text_parts.append(part.get("text", "").strip())
                is_transcript = True

        if text_parts:
            messages.append({
                "author": author_role,
                "content": " ".join(text_parts),
                "is_transcript": is_transcript,
                "timestamp": message_time if author_role == "user" else None  # Seulement pour l'user
            })

    current_node = node.get("parent")

messages.reverse()  # Inversion pour affichage chronologique

# Affichage
print(f"=== Conversation {target_index} ===")
print(f"Title: {title}")
print(f"Create Time: {create_time}")
print(f"Agent: {agent_name} ({gizmo_id})")  # Affiche le nom + ID si connu
print(f"Modèle utilisé: {default_model_slug}")
print(f"Conversation archivée: {'Oui' if is_archived else 'Non'}")
print("Messages:")
for msg in messages:
    transcript_flag = " [Transcript]" if msg["is_transcript"] else ""
    timestamp_info = f" | Timestamp: {msg['timestamp']}" if msg["timestamp"] else ""
    print(f"- {msg['author']}: {msg['content']}{transcript_flag}{timestamp_info}")
