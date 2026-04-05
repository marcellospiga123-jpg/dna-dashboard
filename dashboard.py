from flask import Flask, jsonify, render_template_string
import requests
import base64
import os
import json

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "marcellospiga123-jpg/dna-dashboard"
FILE = "storico.json"

HTML = """
<h1>🚀 DNA Dashboard</h1>
<button onclick="load()">Carica dati</button>
<pre id="out"></pre>

<script>
function load(){
 fetch('/data')
 .then(r=>r.json())
 .then(d=>{
   document.getElementById('out').innerText = JSON.stringify(d,null,2)
 })
}
</script>
"""

@app.route("/")
def home():
    return HTML

@app.route("/data")
def data():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return jsonify({"error": "no data"})

    data = r.json()

    content = base64.b64decode(data["content"]).decode()
    return jsonify(json.loads(content))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
