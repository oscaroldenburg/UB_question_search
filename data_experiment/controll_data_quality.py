import json

FILE = "questions.json"   # ändra om den ligger annan stans

REQUIRED_FIELDS = ["question", "answer_alternatives", "category", "answer_type"]


def main():
    with open(FILE, encoding="utf-8") as f:
        data = json.load(f)

    missing_counts = {field: 0 for field in REQUIRED_FIELDS}

    for entry in data:
        for field in REQUIRED_FIELDS:
            # Räknar som saknas om värdet saknas eller None
            if field not in entry or entry[field] is None or entry[field] == "":
                missing_counts[field] += 1

    missing_by_category = {field: {} for field in REQUIRED_FIELDS}
    for entry in data:
        cat = entry.get("category","UNKNOWN")
        question = entry.get("question","<no question>")
        print(question)
        for field in REQUIRED_FIELDS:
            if field not in entry or entry[field] is None or entry[field] == "":
                missing_by_category[field][cat] = missing_by_category[field].get(cat, 0) + 1

    print("\n===== MISSING FIELD SUMMARY =====\n")
    for field, count in missing_counts.items():
        line = f"{field:<20}: {count}"
        if count > 0:
            breakdown = "   " + " | ".join([f"{cat}:{num}" for cat,num in missing_by_category[field].items()])
            line += "   " + breakdown
        print(line)
    print("\nTotal questions:", len(data))


if __name__ == "__main__":
    main()