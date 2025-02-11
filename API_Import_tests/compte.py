import ijson

json_file = "conversations.json"
count = 0

with open(json_file, "rb") as f:
    for _ in ijson.items(f, "item"):
        count += 1

print(f"Nombre total de conversations : {count}")
