from flask import Flask, jsonify, render_template_string
import requests
import base64
import os
import json

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GH_TOKEN")
REPO = os.getenv("REPO")
FILE = "storico.json"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DNA Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>

<h1>🚀 DNA Dashboard</h1>
<button onclick="load()">Carica dati</button>

<canvas id="chart" width="600" height="300"></canvas>

<pre id="out"></pre>

<script>
async function load() {
    let res = await fetch('/data');
    let data = await res.json();

    document.getElementById('out').innerText =
        JSON.stringify(data, null, 2);

    // GRAFICO
    let labels = [];
    let prezzi = [];

    let first = Object.keys(data)[0];

    if (first) {
        let arr = data[first];

        arr.forEach(x => {
            labels.push(x.data);
            prezzi.push(x.prezzo);
        });
    }

    new Chart(document.getElementById('chart'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Prezzo',
                data: prezzi
            }]
        }
    });
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/data")
def data():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return jsonify({})

    content = base64.b64decode(r.json()["content"]).decode()

    return jsonify(json.loads(content))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
