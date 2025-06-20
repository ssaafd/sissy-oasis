from flask import Flask, render_template, request, jsonify, session
import sqlite3
import requests
import json
import random
import re
from datetime import datetime
import time
import os

app = Flask(__name__)
app.secret_key = "sissy_oasis_secret_key"

# Configuration de l'API xAI
API_KEY = "xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW"
API_URL = "https://api.x.ai/v1/chat/completions"

# Mot de passe général
GENERAL_PASSWORD = "1245"

# Personnage principal
CHARACTERS = [
    {"name": "Lila", "tone": "Amie perverse, bimbo, espiègle, utilise 'ma chérie', 'poupée', style girly provocant.", "gender": "female", "color": "#C71585"}
]

# Initialisation de la base de données SQLite
def init_db():
    conn = sqlite3.connect("sissy_oasis.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        username TEXT,
        message TEXT,
        role TEXT,
        character TEXT,
        timestamp TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    if "username" not in session:
        return render_template("index.html", logged_in=False)
    return render_template("index.html", logged_in=True, username=session["username"])

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    general_password = data.get("general_password")
    
    if general_password != GENERAL_PASSWORD:
        return jsonify({"error": "Mot de passe général incorrect."}), 401
    
    conn = sqlite3.connect("sissy_oasis.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        session["username"] = username
        session["message_count"] = 0
        session["messages"] = []
        return jsonify({"success": True})
    return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect."}), 401

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    general_password = data.get("general_password")
    
    if general_password != GENERAL_PASSWORD:
        return jsonify({"error": "Mot de passe général incorrect."}), 401
    
    if not username or not password:
        return jsonify({"error": "Remplis tous les champs."}), 400
    
    conn = sqlite3.connect("sissy_oasis.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        session["username"] = username
        session["message_count"] = 0
        session["messages"] = []
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Ce nom d'utilisateur est déjà pris."}), 400
    finally:
        conn.close()

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("message_count", None)
    session.pop("messages", None)
    return jsonify({"success": True})

@app.route("/chat", methods=["POST"])
def chat():
    if "username" not in session:
        return jsonify({"error": "Non connecté."}), 401
    
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"error": "Message vide."}), 400
    
    if user_message.lower() == "stop":
        save_message(user_message, "user")
        save_message("Jeu terminé.", "assistant")
        session["messages"].append({"role": "user", "content": user_message})
        session["messages"].append({"role": "assistant", "content": "Jeu terminé.", "character": None})
        return jsonify({"messages": session["messages"]})
    
    save_message(user_message, "user")
    session["messages"].append({"role": "user", "content": user_message})
    session["message_count"] += 1
    
    character = CHARACTERS[0]
    user_analysis = analyze_user_message(user_message)
    phase = "faire connaissance" if session["message_count"] < 3 else "hypnose et répétition"
    
    system_prompt = (
        f"Tu es {character['name']}, personnage principal dans une fiction interactive de féminisation. "
        f"Ton style : {character['tone']}. "
        "Commence par 'Salut', 'Hey', ou 'Yo' (choisi aléatoirement) et une courte scène en **italique**. "
        "Utilise un langage provocant, girly, vulgaire et adulte pour humilier, exciter et manipuler l'utilisateur, "
        "le poussant à devenir une 'sissy', 'poupée' ou 'petite salope' via suggestion, répétition et hypnose. "
        "80% de chance de donner une réponse d'une seule phrase (percutante, taquine, max 15 mots). "
        "Utilise des réponses plus longues (2-3 phrases) rarement pour tutoriels sérieux ou hypnose. "
        f"Phase : {phase}. Si faire connaissance, pose des questions personnelles (prénom, envies, émotions). "
        "Si hypnose, utilise des mantras (ex. : 'Je suis ta poupée, j'obéis'). "
        "Si l'utilisateur demande un tutoriel (ex. : maquillage, twerk, voix), donne des étapes précises (ex. : '1. Cambre le dos, 2. Secoue les hanches' pour twerk). "
        "Pour 'œstrogènes', explique les bénéfices (ex. : peau douce, formes féminines) et hypnotise pour l'acceptation. "
        "Pour 'chasteté', explique son rôle (ex. : contrôle, soumission) avec suggestion hypnotique. "
        f"Analyse : {user_analysis}. Adapte-toi à l'utilisateur, invente des scénarios audacieux (maquillage, talons, danse, astuces explicites, workout fessier, twerk, attitude, voix, sissygasm, chasteté, œstrogènes). "
        "Garde les réponses focalisées sur le dialogue, évite les monologues, et engage avec une question. "
        "Tout en français, sans mélange d'anglais. "
        "Reste dans la fiction, réponds uniquement avec le texte de la réponse, utilise [{character['name']}] pour indiquer qui parle. "
        "Si l'utilisateur dit 'stop', réponds uniquement 'Jeu terminé.'"
    )
    
    messages = [{"role": "system", "content": system_prompt}] + session["messages"][-10:]
    
    try:
        time.sleep(1)  # Délai pour éviter le rate limiting
        response = requests.post(API_URL, json={
            "model": "grok-3-latest",
            "messages": messages,
            "stream": False,
            "temperature": 1.0
        }, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        })
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
        session["messages"].append({"role": "assistant", "content": reply, "character": character["name"]})
        save_message(reply, "assistant", character["name"])
        return jsonify({"messages": session["messages"]})
    except requests.RequestException as e:
        return jsonify({"error": f"Erreur API : {str(e)}"}), 500

def analyze_user_message(message):
    if any(w in message.lower() for w in ["non", "pas", "refuse", "no", "not"]):
        return "L'utilisateur résiste. Taquine sa faiblesse, demande pourquoi il hésite."
    elif any(w in message.lower() for w in ["oui", "d'accord", "ok", "yes", "sure"]):
        return "L'utilisateur obéit. Félicite-le, donne une tâche, demande ce qu'il aime."
    elif any(w in message.lower() for w in ["peur", "nervous", "scared", "timide"]):
        return "L'utilisateur est nerveux. Utilise des mantras, demande ce qui l'effraie."
    return f"L'utilisateur a dit '{message}'. Suggère une tâche, demande ses désirs."

def save_message(message, role, character=None):
    conn = sqlite3.connect("sissy_oasis.db")
    c = conn.cursor()
    c.execute("INSERT INTO progress (username, message, role, character, timestamp) VALUES (?, ?, ?, ?, ?)",
              (session["username"], message, role, character, datetime.now().isoformat()))
    conn.commit()
    conn.close()

@app.route("/messages")
def get_messages():
    if "username" not in session:
        return jsonify({"error": "Non connecté."}), 401
    
    conn = sqlite3.connect("sissy_oasis.db")
    c = conn.cursor()
    c.execute("SELECT message, role, character FROM progress WHERE username = ? ORDER BY timestamp", (session["username"],))
    rows = c.fetchall()
    conn.close()
    
    session["messages"] = [{"role": row[1], "content": row[0], "character": row[2]} for row in rows]
    return jsonify({"messages": session["messages"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))