from flask import Flask, jsonify, render_template_string
import json
import os

app = Flask(__name__)

HTML = """
<h1>🚀 AI Trader Dashboard</h1>
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
    try:
        with open("storico.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
