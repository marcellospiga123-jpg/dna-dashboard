from flask import Flask, render_template_string, jsonify, send_file
import json, os

app = Flask(__name__)

STORICO_FILE = "storico.json"

def load_data():
    if os.path.exists(STORICO_FILE):
        with open(STORICO_FILE) as f:
            return json.load(f)
    return {}

@app.route("/")
def home():
    return render_template_string("""
    <h1>🚀 AI Trader Dashboard</h1>
    <button onclick="load()">Carica dati</button>
    <div id="d"></div>

    <script>
    function load(){
        fetch('/data')
        .then(r=>r.json())
        .then(d=>{
            let html="";
            for(let k in d){
                html+="<p>"+k+"</p>";
            }
            document.getElementById("d").innerHTML=html;
        });
    }
    </script>
    """)

@app.route("/data")
def data():
    return jsonify(load_data())

@app.route("/grafico.png")
def grafico():
    if os.path.exists("grafico.png"):
        return send_file("grafico.png")
    return "no graph",404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))