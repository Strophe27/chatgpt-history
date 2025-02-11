import sqlite3

# Connexion à la base (fichier SQLite)
db_file = "chatgpt_history.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Création de la table des conversations
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    create_time REAL,
    gizmo_id TEXT,
    agent_name TEXT DEFAULT 'Inconnu',
    model TEXT,
    is_archived BOOLEAN DEFAULT 0
);
""")

# Création de la table des messages
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER,
    author TEXT,
    content TEXT,
    message_time REAL,
    is_transcript BOOLEAN DEFAULT 0,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
""")

# Création de la table des agents (associe gizmo_id à un nom)
cursor.execute("""
CREATE TABLE IF NOT EXISTS agents (
    gizmo_id TEXT PRIMARY KEY,
    agent_name TEXT
);
""")

# Validation et fermeture
conn.commit()
conn.close()

print("📌 Base de données SQLite initialisée avec succès !")
