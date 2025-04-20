import json
import csv
import re

# === Tag mapping ===
TAG_MAP = {
    "[gf]": "gluten free",
    "[v]": "vegan",
    "[veg]": "vegetarian",
    "[nuts]": "contains nuts",
    "[h]": "halal",
    "[halal]": "halal",
    "[vegan]": "vegan"
}

def expand_tags(tag_list):
    """Expand tags like [gf] into full phrases."""
    if not tag_list:
        return []
    expanded = []
    for tag in tag_list:
        parts = re.findall(r"\[[^\]]+\]", tag.lower())
        for p in parts:
            if p in TAG_MAP:
                expanded.append(TAG_MAP[p])
    return list(dict.fromkeys(expanded))

def normalize(text):
    """Remove line breaks and non-breaking spaces."""
    return text.replace("\u00a0", " ").replace("\n", " ").strip() if text else ""

# === Load JSON ===
with open("rasa_data_cleaned.json", "r") as f:
    data = json.load(f)

restaurant = data["restaurant"]
contact_info = data.get("contact_info", "")

# Flatten location info (we’ll map each item to all locations)
locations = data.get("locations", [])
default_state = None
if locations and locations[0]["state"] is None:
    locations = locations[1:]  # Remove "visit our 5 locations" header

# === Convert to rows ===
rows = []
for item in data["menu"]:
    name = normalize(item.get("name"))
    category = normalize(item.get("category"))
    description = normalize(item.get("description"))
    options = ", ".join([normalize(opt) for opt in item.get("options", [])])
    tags = item.get("tag", [])
    tags = tags if isinstance(tags, list) else [tags]
    tag_str = ", ".join(expand_tags(tags))

    # Map each item to every location (can customize to be 1-to-1 if needed)
    for loc in locations:
        rows.append({
            "restaurant": restaurant,
            "category": category,
            "item_name": name,
            "description": description,
            "options": options,
            "tags": tag_str,
            "state": loc.get("state", ""),
            "address": loc.get("address", ""),
            "contact_info": contact_info
        })

# === Write CSV ===
with open("rasa_data_flat.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("✅ CSV saved as 'rasa_data_flat.csv'")
