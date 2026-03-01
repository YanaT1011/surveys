import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import csv
from pathlib import Path

app = Flask(__name__, template_folder="../templates")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FORMS_CSV = DATA_DIR / "forms.csv"
ANSWERS_CSV = DATA_DIR / "answers.csv"

# Создаём файл ответов, если его нет
if not ANSWERS_CSV.exists():
    with open(ANSWERS_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "form_id", "question", "answer"])

# Загружаем данные форм
def load_forms():
    forms = {}
    with open(FORMS_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            forms[row["form_id"]] = row
    return forms

@app.route("/form/<form_id>", methods=["GET", "POST"])
def show_form(form_id):
    forms = load_forms()
    if form_id not in forms:
        return "Анкета не найдена", 404

    form = forms[form_id]

    # Проверяем лимит
    last_question_name = "q17"  # имя последнего вопроса

    current_count = 0

    with open(ANSWERS_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        current_count = sum(
            1 for row in reader
            if row
            and row.get("form_id") == form_id
            and row.get("question") == last_question_name
        )

        if int(form["max_answers"]) <= current_count:
            return "Лимит ответов достигнут", 403

    if request.method == "POST":
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        with open(ANSWERS_CSV, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)

            for question, answer in request.form.items():
                writer.writerow([
                    timestamp,
                    form_id,
                    question,
                    answer
                ])

        return redirect(url_for("thank_you"))

    return render_template("school.html", form_name=form["form_name"])

@app.route("/thank-you")
def thank_you():
    return "Спасибо! Ваш ответ сохранён. Страницу можно закрыть."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)