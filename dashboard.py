from flask import Flask, jsonify
import requests, base64, json, os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("REPO")

@app.route("/data")
def data():
    url = f"https://api.github.com/repos/{REPO}/contents/storico.json"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return jsonify([])

    content = base64.b64decode(r.json()["content"]).decode()
    storico = json.loads(content)

    out = []

    for nome, v in storico.items():
        prezzi = [x["prezzo"] for x in v if x["prezzo"] > 0]
        if not prezzi:
            continue

        attuale = prezzi[-1]
        max_p = max(prezzi)
        min_p = min(prezzi)
        roi = ((max_p - attuale) / attuale * 100)

        out.append({
            "nome": nome,
            "attuale": attuale,
            "roi": round(roi, 2)
        })

    return jsonify(out)

@app.route("/")
def home():
    return """
    <h1>🚀 DNA DASHBOARD PRO</h1>
    <button onclick="load()">Carica</button>
    <pre id="out"></pre>

    <script>
    async function load(){
        let r = await fetch('/data');
        let d = await r.json();
        document.getElementById('out').innerText = JSON.stringify(d,null,2);
    }
    </script>
    """

app.run()
