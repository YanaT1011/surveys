import csv
from pathlib import Path
import uuid

CSV_FILE = Path("../data/forms.csv")

if not CSV_FILE.exists():
    print("CSV файл не найден!")
    exit()

# --- Читаем все строки ---
rows = []
with open(CSV_FILE, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Если ID пустой, генерируем
        if not row["form_id"]:
            row["form_id"] = uuid.uuid4().hex[:8]
        # Генерируем ссылку
        row["link"] = f"/form/{row['form_id']}"
        rows.append(row)

# --- Записываем обратно в CSV ---
with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("CSV обновлён. Вот новые ссылки для форм:")
for row in rows:
    print(f"{row['form_name']} → {row['link']}")