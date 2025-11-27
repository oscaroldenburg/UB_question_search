import json
import openpyxl
from pathlib import Path


EXCEL_FILE = "../api/Frågenyckel - Telekom 02-25 - test.xlsx"
OUTPUT_JSON = "questions.json"
ANSWER_TYPE_MAP = {
    # 🟩 singel – båda gröna varianter
    "FF92D050": "singel",
    "FF00FF00": "singel",   # om denna förekommer

    # 🟦 multi – blå toner
    "FF3333FF": "multi",    # ljusare blå
    "FF002060": "multi",    # mörkare blå

    # 🟪 numerisk
    "FF7030A0": "numerisk",

    # 🟨 loop
    "FFFFC000": "loop",

    # 🔴 skala
    "FFFF0000": "skala",
    "FF0000D4": "skala",

    # ⚫ 3D-skala
    "FF000000": "skala_3d",

    # 🟡 fritext
    "FFFFFF00": "öppen",

    # ⚙️ uteslutande (gissad grå)
    "FF7F7F7F": "uteslutande",

    "00000000": None,  # ingen färg
}


def get_fill_color(cell):
    """
    Försöker extrahera en RGB-färgkod från cellens fyllning.
    Returnerar t.ex. 'FFFF0000' eller None om ingen färg hittas.
    """
    """ answerTypeMap = {
        "singel":  """
    
    fill = cell.fill
    if fill is None:
        return None

    # openpyxl använder fgColor / start_color
    color = getattr(fill, "fgColor", None)
    if color is not None and getattr(color, "type", None) == "rgb":
        try:
            return ANSWER_TYPE_MAP[color.rgb]
        except KeyError:
            print("Unknown color code:", color.rgb)

    start_color = getattr(fill, "start_color", None)
    if start_color is not None and getattr(start_color, "type", None) == "rgb":
        try:
            return ANSWER_TYPE_MAP[start_color.rgb]
        except KeyError:
            print("Unknown start color code:", start_color.rgb)

    return None
    


def extract_questions_from_workbook(xlsx_path: str):
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    all_questions = []
    ws = wb.active


    for ws in wb.worksheets:
        category = ws.title
        max_row = ws.max_row
        max_col = ws.max_column

        for row in range(1, max_row + 1):
            q_cell = ws[f"F{row}"]
            value = q_cell.value

            if value is None:
                continue

            text = str(value).strip()
            is_bold = bool(q_cell.font and q_cell.font.bold)

            # Villkor för att en cell ska räknas som fråga
            if not is_bold:
                continue
            if "?" not in text and "..." not in text:
                continue

            question = text

            # --- Hämta svarsalternativ ---
            answer_alternatives = []
            alt_row = row
            answer_type_color = get_fill_color(ws[f"D{row}"])

            if alt_row >= 1 and answer_type_color != "öppen":

                # Kolumn H = index 8, sedan åt höger tills tom cell
                while True:
                    alt_cell = ws.cell(row=alt_row, column=8)
                    alt_val = alt_cell.value

                    if alt_val is None or str(alt_val).strip() == "":
                        if alt_row == row:
                            alt_row += 1
                            continue
                        else:
                            break
                    answer_alternatives.append(str(alt_val).strip())
                    alt_row += 1

            # Free_Text: True om inga svarsalternativ hittades

            # Answer_type via färg i kolumn D på samma rad

            question_obj = {
                "question": question,
                "answer_alternatives": answer_alternatives,
                "category": category,
                "answer_type": answer_type_color,  # här kan du senare mappa färg -> "singel"/"multi"
            }

            all_questions.append(question_obj)

    return all_questions


def main():
    xlsx_path = Path(EXCEL_FILE)
    if not xlsx_path.is_file():
        raise FileNotFoundError(f"Hittar inte filen: {xlsx_path.resolve()}")

    data = extract_questions_from_workbook(str(xlsx_path))

    # Spara till JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Klart! Extraherade {len(data)} frågor.")
    print(f"JSON sparad som: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()