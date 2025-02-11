import ijson

# Chemin du fichier JSON
json_file = "conversations.json"

# Lecture en streaming pour éviter de charger le fichier en mémoire
with open(json_file, "rb") as f:
    parser = ijson.items(f, "item")
    first_conversation = next(parser, None)  # Prendre la première conversation

# Vérification si une conversation est trouvée
if not first_conversation:
    print("Aucune conversation trouvée.")
    exit()

# Extraction des informations principales
title = first_conversation.get("title", "Sans titre")
create_time = first_conversation.get("create_time", "Inconnu")
mapping = first_conversation.get("mapping", {})

# Vérification du nombre de nœuds
print(f"DEBUG: mapping contient {len(mapping)} éléments")

# Récupération du premier message en suivant `current_node`
current_node = first_conversation.get("current_node")
messages = []

while current_node:
    node = mapping.get(current_node)
    if not node:
        break  # Si le nœud est invalide, arrêter la boucle

    message_data = node.get("message")

    if message_data:
        author_role = message_data.get("author", {}).get("role", "inconnu")
        content_obj = message_data.get("content", {})
        parts = content_obj.get("parts", [])

        text_parts = []
        is_transcript = False

        for part in parts:
            if isinstance(part, str) and part.strip():
                text_parts.append(part.strip())
            elif isinstance(part, dict):
                if part.get("content_type") == "audio_transcription":
                    text_parts.append(part.get("text", "").strip())
                    is_transcript = True

        # Ajout du message uniquement si du texte est présent
        if text_parts:
            messages.append({
                "author": author_role,
                "content": " ".join(text_parts),
                "is_transcript": is_transcript
            })

    # Passage au parent
    current_node = node.get("parent")

# Inverser l'ordre des messages pour affichage chronologique
messages.reverse()

# Affichage des résultats
print("=== Première Conversation ===")
print(f"Title: {title}")
print(f"Create Time: {create_time}")
print("Messages:")
for msg in messages:
    transcript_flag = " [Transcript]" if msg["is_transcript"] else ""
    print(f"- {msg['author']}: {msg['content']}{transcript_flag}")
