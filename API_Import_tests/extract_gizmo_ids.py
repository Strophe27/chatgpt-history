import ijson
from collections import defaultdict

# Chemin du fichier JSON
json_file = "conversations.json"

# Dictionnaire pour compter les occurrences des gizmo_id
gizmo_counts = defaultdict(int)

# Lecture en streaming
with open(json_file, "rb") as f:
    parser = ijson.items(f, "item")  # Parcourt chaque conversation

    for conversation in parser:
        gizmo_id = conversation.get("gizmo_id", "Inconnu")
        gizmo_counts[gizmo_id] += 1  # Incrémente le compteur pour ce gizmo_id

# Tri des gizmo_id par nombre d'apparitions (descendant)
sorted_gizmo = sorted(gizmo_counts.items(), key=lambda x: x[1], reverse=True)

# Affichage des résultats
print("=== Liste des Agents (gizmo_id) ===")
for gizmo_id, count in sorted_gizmo:
    print(f"- {gizmo_id}: {count} conversation(s)")
