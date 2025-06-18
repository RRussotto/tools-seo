from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/performance")
def performance():
    url = request.args.get("url")
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {"url": url, "strategy": "mobile"}
    r = requests.get(api_url, params=params)
    return jsonify(r.json())

@app.route("/api/keywords")
def keywords():
    query = request.args.get("query")
    headers = {"X-Twaip-Key": "YOUR_TWINWORD_API_KEY"}
    r = requests.get("https://api.twinword.com/api/keyword/related", headers=headers, params={"entry": query})
    return jsonify(r.json())

@app.route("/api/gsc")
def gsc():
    return jsonify({"error": "Richiede autenticazione OAuth lato server."})

if __name__ == "__main__":
    app.run(debug=True)
