from flask import Flask, request
import os
from google import genai

app = Flask(__name__)

# ✅ Create Gemini client ONCE
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        q = request.form.get("q")

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=q
            )
            answer = response.text
        except Exception as e:
            answer = f"Gemini error: {e}"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SASI AI Search</title>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg,#667eea,#764ba2);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .box {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                width: 420px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,.2);
            }}
            input {{
                width: 100%;
                padding: 12px;
                margin-top: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }}
            button {{
                width: 100%;
                margin-top: 15px;
                padding: 12px;
                border: none;
                border-radius: 8px;
                background: #4f46e5;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}
            .answer {{
                margin-top: 20px;
                padding: 15px;
                background: #f3f4f6;
                border-radius: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🤖 SASI AI Search</h2>
            <form method="POST">
                <input name="q" placeholder="Ask anything..." required>
                <button>Search</button>
            </form>
            {f"<div class='answer'><b>Answer:</b><br>{answer}</div>" if answer else ""}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
