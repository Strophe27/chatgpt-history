import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base de données
DB_FILE = "chatgpt_history.db"
conn = sqlite3.connect(DB_FILE)

# Charger les conversations dans un DataFrame Pandas
df = pd.read_sql_query("SELECT create_time, agent_name, model FROM conversations", conn)
conn.close()

# Convertir les timestamps en dates lisibles
df["create_date"] = pd.to_datetime(df["create_time"], unit="s").dt.date

# 📊 1. Graphique des conversations par jour
df_day = df.groupby("create_date").size()
plt.figure(figsize=(10, 5))
df_day.plot(kind="bar", title="Nombre de conversations par jour")
plt.xticks(rotation=45)
plt.ylabel("Nombre de conversations")
plt.savefig("conversations_par_jour.png")

# 📊 2. Répartition des agents utilisés
df_agents = df["agent_name"].value_counts()
plt.figure(figsize=(8, 5))
df_agents.plot(kind="pie", title="Répartition des agents", autopct="%1.1f%%")
plt.ylabel("")
plt.savefig("repartition_agents.png")

# 📊 3. Répartition des modèles GPT utilisés
df_models = df["model"].value_counts()
plt.figure(figsize=(8, 5))
df_models.plot(kind="bar", title="Répartition des modèles GPT")
plt.xticks(rotation=45)
plt.ylabel("Nombre de conversations")
plt.savefig("repartition_modeles.png")

print("✅ Graphiques générés : conversations_par_jour.png, repartition_agents.png, repartition_modeles.png")
