import os
print("APP FILE:", __file__)
print("CWD:", os.getcwd())


from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

# ------------------ CONFIG ------------------

app = Flask(__name__)

# Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Database file
DB_NAME = "users.db"

# ------------------ DATABASE ------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_search(query, result):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO searches (query, result) VALUES (?, ?)",
              (query, result))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT query, result FROM searches ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# ------------------ GEMINI SEARCH ------------------

def ai_search(query):
    api_key = os.getenv("GEMINI_API_KEY")

    # ✅ If API key is NOT set (Render), do not crash
    if not api_key:
        return f"You searched for: {query}"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(query)
    return response.text


# ------------------ ROUTES ------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("search"))
    return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    result = None
    if request.method == "POST":
        query = request.form.get("query")
        result = ai_search(query)
        save_search(query, result)
    return render_template("search.html", result=result)

@app.route("/history")
def history():
    data = get_history()
    return render_template("history.html", data=data)

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(debug=True)
