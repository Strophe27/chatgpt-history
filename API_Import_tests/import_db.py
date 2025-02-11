import sqlite3
import ijson
import decimal  # Import pour gérer les valeurs Decimal

# Chemin du fichier JSON et de la base SQLite
json_file = "conversations.json"
db_file = "chatgpt_history.db"

# Connexion à la base
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Lecture en streaming du fichier JSON
with open(json_file, "rb") as f:
    parser = ijson.items(f, "item")

    for conv in parser:
        # Extraction des infos principales
        title = conv.get("title", "Sans titre")
        create_time = conv.get("create_time", None)
        gizmo_id = conv.get("gizmo_id", "Inconnu")
        model = conv.get("default_model_slug", "Inconnu")
        is_archived = int(conv.get("is_archived", False))  # Convertir en 0 ou 1

        # Conversion sécurisée des timestamps en float
        create_time = float(create_time) if isinstance(create_time, (float, decimal.Decimal)) else None

        # Vérifier si l'agent est déjà enregistré
        cursor.execute("SELECT agent_name FROM agents WHERE gizmo_id = ?", (gizmo_id,))
        agent_entry = cursor.fetchone()
        agent_name = agent_entry[0] if agent_entry else gizmo_id  # Si inconnu, garder l'ID

        # Insérer ou mettre à jour l'agent
        cursor.execute("INSERT OR IGNORE INTO agents (gizmo_id, agent_name) VALUES (?, ?)", (gizmo_id, agent_name))

        # Insérer la conversation sans contenu pour le moment
        cursor.execute("""
            INSERT INTO conversations (title, create_time, gizmo_id, agent_name, model, is_archived, content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, create_time, gizmo_id, agent_name, model, is_archived, ""))

        # Récupérer l'ID de la conversation insérée
        conversation_id = cursor.lastrowid

        # Extraction des messages et construction du contenu
        mapping = conv.get("mapping", {})
        messages = []
        full_content = []

        for node in mapping.values():  # 🔄 Parcours de tous les messages
            message_data = node.get("message")
            if message_data:
                author_role = message_data.get("author", {}).get("role", "inconnu")
                message_time = message_data.get("create_time", None)
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
                    message_text = " ".join(text_parts)
                    message_time = float(message_time) if isinstance(message_time, (float, decimal.Decimal)) else None
                    messages.append((conversation_id, author_role, message_text, message_time, int(is_transcript)))

                    # ✅ Ajouter au contenu global
                    full_content.append(f"{author_role}: {message_text}")

        # Insérer les messages associés
        cursor.executemany("""
            INSERT INTO messages (conversation_id, author, content, message_time, is_transcript)
            VALUES (?, ?, ?, ?, ?)
        """, messages)

        # ✅ Mise à jour du `content` avec tous les messages concaténés
        full_content_text = "\n".join(full_content)
        cursor.execute("""
            UPDATE conversations SET content = ? WHERE id = ?
        """, (full_content_text, conversation_id))

        conn.commit()  # Valider après chaque conversation

# Fermeture de la base
conn.close()

print("✅ Importation des conversations et messages terminée avec succès !")
