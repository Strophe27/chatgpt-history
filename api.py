from fastapi import FastAPI, Query, HTTPException
import sqlite3
from collections import defaultdict
from datetime import datetime
from collections import defaultdict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DB_FILE = "chatgpt_history.db"

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autoriser React
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

class UpdateAgentRequest(BaseModel):
    id: int
    agent_name: str

class ToggleArchiveRequest(BaseModel):
    id: int

# Modifier l'agent d'une conversation
@app.post("/update_agent")
def update_agent(data: UpdateAgentRequest):
    conn = sqlite3.connect("chatgpt_history.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET agent_name = ? WHERE id = ?", (data.agent_name, data.id))
    conn.commit()
    conn.close()
    return {"message": "Agent mis à jour"}

# Archiver/Désarchiver une conversation
@app.post("/toggle_archive")
def toggle_archive(data: ToggleArchiveRequest):
    conn = sqlite3.connect("chatgpt_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT is_archived FROM conversations WHERE id = ?", (data.id,))
    row = cursor.fetchone()
    if row:
        new_status = 0 if row[0] == 1 else 1
        cursor.execute("UPDATE conversations SET is_archived = ? WHERE id = ?", (new_status, data.id))
        conn.commit()
    conn.close()
    return {"message": "Statut archivé mis à jour"}

# Récupérer les conversations avec filtres
@app.get("/conversations")
def list_conversations(
    gizmo_id: str = Query(None, description="Filtrer par agent"),
    is_archived: int = Query(None, description="0 = actif, 1 = archivé"),
    start_time: float = Query(None, description="Timestamp début"),
    end_time: float = Query(None, description="Timestamp fin")
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Construction dynamique de la requête SQL
    query = "SELECT id, title, create_time, gizmo_id, agent_name, model, is_archived FROM conversations WHERE 1=1"
    params = []

    if gizmo_id:
        query += " AND gizmo_id = ?"
        params.append(gizmo_id)

    if is_archived is not None:
        query += " AND is_archived = ?"
        params.append(is_archived)

    if start_time and end_time:
        query += " AND create_time BETWEEN ? AND ?"
        params.append(start_time)
        params.append(end_time)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "create_time": row[2], "gizmo_id": row[3], "agent_name": row[4], "model": row[5], "is_archived": bool(row[6])}
        for row in rows
    ]

# Récupérer une conversation spécifique avec son contenu
@app.get("/conversation/{conv_id}")
def get_conversation(conv_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, create_time, gizmo_id, agent_name, model, is_archived, content FROM conversations WHERE id = ?", (conv_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Conversation non trouvée")
    
    return {
        "id": row[0], 
        "title": row[1], 
        "create_time": row[2], 
        "gizmo_id": row[3], 
        "agent_name": row[4], 
        "model": row[5], 
        "is_archived": bool(row[6]),
        "content": row[7] if row[7] else "🚨 Aucun contenu disponible."
    }


# Filtrer les conversations par agent
@app.get("/conversations/agent/{gizmo_id}")
def get_conversations_by_agent(gizmo_id: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE gizmo_id = ?", (gizmo_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"id": row[0], "title": row[1], "create_time": row[2], "gizmo_id": row[3], "agent_name": row[4], "model": row[5], "is_archived": bool(row[6])}
        for row in rows
    ]

# Modifier un agent (mise à jour dans `agents` et `conversations`)
@app.put("/agents/{gizmo_id}")
def update_agent_name(gizmo_id: str, new_name: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Mettre à jour le nom de l'agent dans la table `agents`
    cursor.execute("UPDATE agents SET agent_name = ? WHERE gizmo_id = ?", (new_name, gizmo_id))

    # Mettre à jour le nom de l'agent dans `conversations`
    cursor.execute("UPDATE conversations SET agent_name = ? WHERE gizmo_id = ?", (new_name, gizmo_id))

    conn.commit()
    conn.close()
    
    return {"message": f"Agent {gizmo_id} renommé en {new_name} dans toute la base."}


from collections import defaultdict
from datetime import datetime  # ✅ Import du module manquant

# Route pour récupérer le nombre de conversations par jour
@app.get("/stats/conversations_per_day")
def conversations_per_day():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Récupérer toutes les dates de création
    cursor.execute("SELECT create_time FROM conversations")
    rows = cursor.fetchall()
    conn.close()

    # Transformer les timestamps en date simple (YYYY-MM-DD)
    counts = defaultdict(int)
    for row in rows:
        timestamp = row[0]
        if timestamp:
            date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
            counts[date] += 1

    # Transformer le dictionnaire en liste triée
    sorted_counts = sorted(counts.items(), key=lambda x: x[0])

    return [{"date": date, "count": count} for date, count in sorted_counts]

@app.get("/test_sql")
def test_sql():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, create_time, folder FROM conversations LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    return rows


# Route pour récupérer des statistiques générales
@app.get("/stats")
def get_global_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1️⃣ Nombre total de conversations
    cursor.execute("SELECT COUNT(*) FROM conversations")
    total_conversations = cursor.fetchone()[0]

    # 2️⃣ Nombre de conversations archivées et actives
    cursor.execute("SELECT COUNT(*) FROM conversations WHERE is_archived = 1")
    archived_conversations = cursor.fetchone()[0]
    active_conversations = total_conversations - archived_conversations

    # 3️⃣ Top 5 des agents (`gizmo_id`) les plus utilisés
    cursor.execute("""
        SELECT agent_name, COUNT(*) AS count FROM conversations
        WHERE agent_name IS NOT NULL AND agent_name != ''
        GROUP BY agent_name ORDER BY count DESC LIMIT 5
    """)
    top_agents = [{"agent": row[0], "count": row[1]} for row in cursor.fetchall()]

    # 4️⃣ Répartition des modèles utilisés
    cursor.execute("""
        SELECT model, COUNT(*) AS count FROM conversations
        WHERE model IS NOT NULL AND model != ''
        GROUP BY model ORDER BY count DESC
    """)
    model_distribution = [{"model": row[0], "count": row[1]} for row in cursor.fetchall()]

    conn.close()

    return {
        "total_conversations": total_conversations,
        "active_conversations": active_conversations,
        "archived_conversations": archived_conversations,
        "top_agents": top_agents,
        "model_distribution": model_distribution
    }
