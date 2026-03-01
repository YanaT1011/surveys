import csv
import uuid
from pathlib import Path

# Путь к CSV
CSV_FILE = Path("../data/forms.csv")

# Проверяем, что файл существует
if not CSV_FILE.exists():
    print("CSV файл не найден!")
    exit()

links = []

with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Генерируем уникальный ID формы
        form_id = uuid.uuid4().hex[:8]
        row["form_id"] = form_id

        # Генерируем ссылку
        link = f"/form/{form_id}"
        row["link"] = link

        links.append({
            "form_name": row["form_name"],
            "link": link
        })

# Выводим результат
print("Созданы анкеты:")
for l in links:
    print(f"{l['form_name']} → {l['link']}")