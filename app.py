from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/performance")
def performance():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    api_key = os.environ.get("PAGESPEED_API_KEY")
    if not api_key:
        return jsonify({"error": "API Key non configurata"}), 500

    try:
        api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": url,
            "strategy": "mobile",
            "key": api_key
        }
        r = requests.get(api_url, params=params)
        data = r.json()
        
        if "error" in data:
            return jsonify({"error": data["error"]["message"]}), 429

        return data, r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/keywords")
def keywords():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    try:
        headers = {"X-Twaip-Key": os.environ.get("TWINWORD_API_KEY")}
        r = requests.get("https://api.twinword.com/api/keyword/related", headers=headers, params={"entry": query})
        return r.json(), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

