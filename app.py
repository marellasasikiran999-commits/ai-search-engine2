from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # dummy login (no auth yet)
        return redirect(url_for("search"))
    return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    result = ""
    if request.method == "POST":
        query = request.form.get("query")
        result = f"You searched for: {query}"
    return render_template("search.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
