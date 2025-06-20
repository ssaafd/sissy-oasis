import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import requests
import json
import random
import re
from datetime import datetime
import time

# Configuration de l'API xAI
API_KEY = "xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW"
API_URL = "https://api.x.ai/v1/chat/completions"

# Mot de passe général
GENERAL_PASSWORD = "1245"

# Dictionnaire de traductions
TRANSLATIONS = {
    "fr": {
        "choose_language": "Choisis ta langue, ma puce 💕",
        "select_language": "Sélectionner",
        "enter_password": "Entre le mot de passe général, chérie 💋",
        "password_label": "Mot de passe",
        "submit_password": "Valider ✨",
        "invalid_password": "Mot de passe incorrect, essaie encore !",
        "welcome": "Entre dans SISSY OASIS, ma poupée 💋",
        "username_label": "Ton prénom, chérie",
        "password_user_label": "Mot de passe, ma belle",
        "login": "Se connecter 💕",
        "signup": "S'inscrire ✨",
        "empty_fields": "Remplis tous les champs, ma puce !",
        "username_taken": "Ce prénom est déjà pris.",
        "invalid_login": "Prénom ou mot de passe incorrect.",
        "title": "SISSY OASIS 💖",
        "send": "Envoyer 💋",
        "signout": "Déconnexion ✨",
        "game_over": "Jeu terminé.",
        "api_error": "Erreur API : {error}"
    },
    "en": {
        "choose_language": "Choose your language, darling 💕",
        "select_language": "Select",
        "enter_password": "Enter the general password, sweetie 💋",
        "password_label": "Password",
        "submit_password": "Submit ✨",
        "invalid_password": "Wrong password, try again!",
        "welcome": "Welcome to SISSY OASIS, my doll 💋",
        "username_label": "Your name, honey",
        "password_user_label": "Password, my beauty",
        "login": "Log in 💕",
        "signup": "Sign up ✨",
        "empty_fields": "Fill all fields, sweetie!",
        "username_taken": "This name is already taken.",
        "invalid_login": "Name or password incorrect.",
        "title": "SISSY OASIS 💖",
        "send": "Send 💋",
        "signout": "Sign out ✨",
        "game_over": "Game over.",
        "api_error": "API error: {error}"
    },
    "es": {
        "choose_language": "Elige tu idioma, cariño 💕",
        "select_language": "Seleccionar",
        "enter_password": "Ingresa la contraseña general, pequeña 💋",
        "password_label": "Contraseña",
        "submit_password": "Enviar ✨",
        "invalid_password": "¡Contraseña incorrecta, intenta de nuevo!",
        "welcome": "Bienvenida a SISSY OASIS, mi muñeca 💋",
        "username_label": "Tu nombre, querida",
        "password_user_label": "Contraseña, mi bella",
        "login": "Iniciar sesión 💕",
        "signup": "Registrarse ✨",
        "empty_fields": "¡Rellena todos los campos, pequeña!",
        "username_taken": "Este nombre ya está tomado.",
        "invalid_login": "Nombre o contraseña incorrectos.",
        "title": "SISSY OASIS 💖",
        "send": "Enviar 💋",
        "signout": "Cerrar sesión ✨",
        "game_over": "Juego terminado.",
        "api_error": "Error de API: {error}"
    }
}

# Personnage principal
CHARACTERS = [
    {"name": "Lila", "tone": "Amie perverse, bimbo, espiègle, utilise 'ma chérie', 'poupée', style girly provocant.", "gender": "female", "color": "#C71585"}  # Rose foncé
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

# Classe principale de l'application
class SissyOasis:
    def __init__(self, root):
        self.root = root
        self.root.title("SISSY OASIS 💖")
        self.root.geometry("800x600")
        self.root.configure(bg="#ffeacc")
        self.current_user = None
        self.messages = []
        self.language = "fr"
        self.translations = TRANSLATIONS["fr"]
        self.message_count = 0
        
        self.font = ("Arial", 14)
        self.title_font = ("Arial", 22, "bold")
        
        init_db()
        self.show_language_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_language_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#ffeacc")
        frame.pack(pady=50, padx=50, fill="both", expand=True)
        
        tk.Label(frame, text=TRANSLATIONS["fr"]["choose_language"], font=self.title_font, bg="#ffeacc", fg="#ff69b4").pack(pady=20)
        tk.Button(frame, text="Français", font=self.font, bg="#ff69b4", fg="white", command=lambda: self.set_language("fr")).pack(pady=5, fill="x")
        tk.Button(frame, text="English", font=self.font, bg="#ba55d3", fg="white", command=lambda: self.set_language("en")).pack(pady=5, fill="x")
        tk.Button(frame, text="Español", font=self.font, bg="#00ced1", fg="white", command=lambda: self.set_language("es")).pack(pady=5, fill="x")

    def set_language(self, lang):
        self.language = lang
        self.translations = TRANSLATIONS[lang]
        self.show_password_screen()

    def show_password_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#ffeacc")
        frame.pack(pady=50, padx=20, fill="both", expand=True)
        
        tk.Label(frame, text=self.translations["enter_password"], font=self.title_font, bg="#ffeacc", fg="#ff69b4").pack(pady=20)
        tk.Label(frame, text=self.translations["password_label"], font=self.font, bg="#ffeacc", fg="#4b0082").pack()
        self.general_password_entry = tk.Entry(frame, font=self.font, show="*", bg="#f3e5f5", width=30)
        self.general_password_entry.pack(pady=5)
        tk.Button(frame, text=self.translations["submit_password"], font=self.font, bg="#ff69b4", fg="white", command=self.check_general_password).pack(pady=10)
        self.error_label = tk.Label(frame, text="", font=self.font, bg="#ffeacc", fg="red")
        self.error_label.pack(pady=10)

    def check_general_password(self):
        if self.general_password_entry.get() == GENERAL_PASSWORD:
            self.show_login_screen()
        else:
            self.error_label.config(text=self.translations["invalid_password"])

    def show_login_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#ffeacc")
        frame.pack(pady=50, padx=20, fill="both", expand=True)
        
        tk.Label(frame, text=self.translations["welcome"], font=self.title_font, bg="#ffeacc", fg="#ff69b4").pack(pady=20)
        tk.Label(frame, text=self.translations["username_label"], font=self.font, bg="#ffeacc", fg="#4b0082").pack()
        self.username_entry = tk.Entry(frame, font=self.font, bg="#f3e5f5", width=30)
        self.username_entry.pack(pady=5)
        tk.Label(frame, text=self.translations["password_user_label"], font=self.font, bg="#ffeacc", fg="#4b0082").pack()
        self.password_entry = tk.Entry(frame, font=self.font, show="*", bg="#f3e5f5", width=30)
        self.password_entry.pack(pady=5)
        tk.Button(frame, text=self.translations["login"], font=self.font, bg="#ff69b4", fg="white", command=self.login).pack(pady=10)
        tk.Button(frame, text=self.translations["signup"], font=self.font, bg="#ba55d3", fg="white", command=self.signup).pack(pady=5)
        self.error_label = tk.Label(frame, text="", font=self.font, bg="#ffeacc", fg="red")
        self.error_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = sqlite3.connect("sissy_oasis.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            self.current_user = username
            self.load_progress()
            self.show_game_screen()
            self.start_auto_conversation()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            self.error_label.config(text=self.translations["empty_fields"])
            return
        
        conn = sqlite3.connect("sissy_oasis.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            self.current_user = username
            self.show_game_screen()
            self.start_auto_conversation()
        except sqlite3.IntegrityError:
            self.error_label.config(text=self.translations["username_taken"])
        finally:
            conn.close()

    def load_progress(self):
        conn = sqlite3.connect("sissy_oasis.db")
        c = conn.cursor()
        c.execute("SELECT message, role, character FROM progress WHERE username = ? ORDER BY timestamp", (self.current_user,))
        rows = c.fetchall()
        conn.close()
        self.messages = [{"role": row[1], "content": row[0], "character": row[2]} for row in rows]

    def save_progress(self, message, role, character=None):
        conn = sqlite3.connect("sissy_oasis.db")
        c = conn.cursor()
        c.execute("INSERT INTO progress (username, message, role, character, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (self.current_user, message, role, character, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def show_game_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg="#ffeacc")
        frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        tk.Label(frame, text=self.translations["title"], font=self.title_font, bg="#ffeacc", fg="#ff69b4").pack(pady=10)
        self.chat_area = scrolledtext.ScrolledText(frame, font=self.font, bg="#f3e5f5", fg="#4b0082", height=20, wrap=tk.WORD)
        self.chat_area.pack(pady=10, fill="both", expand=True)
        self.chat_area.config(state="disabled")
        
        input_frame = tk.Frame(frame, bg="#ffeacc")
        input_frame.pack(fill="x", pady=5)
        self.input_entry = tk.Entry(input_frame, font=self.font, bg="#f3e5f5", width=50)
        self.input_entry.pack(side="left", padx=5)
        self.input_entry.bind("<Return>", lambda event: self.send_message())
        tk.Button(input_frame, text=self.translations["send"], font=self.font, bg="#ff69b4", fg="white", command=self.send_message).pack(side="left", padx=5)
        
        tk.Button(frame, text=self.translations["signout"], font=self.font, bg="#ba55d3", fg="white", command=self.show_language_screen).pack(pady=5)
        
        for msg in self.messages:
            self.display_message(msg)

    def display_message(self, msg):
        self.chat_area.config(state="normal")
        if msg["role"] == "user":
            self.chat_area.insert(tk.END, f"Vous: {msg['content']}\n", "user")
        else:
            character = CHARACTERS[0]  # Lila
            color = character["color"]
            lines = msg["content"].split("\n")
            for line in lines:
                if re.match(r"\*\*.*\*\*", line):
                    scene = line.strip("**").strip("*")
                    self.chat_area.insert(tk.END, f"{scene}\n", "scene")
                else:
                    self.chat_area.insert(tk.END, f"{line}\n", f"character_{color}")
            self.chat_area.tag_configure(f"character_{color}", foreground=color)
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)
        self.chat_area.tag_configure("user", foreground="#ff1493", justify="right")
        self.chat_area.tag_configure("scene", foreground="#4682b4", font=("Arial", 14, "italic"))

    def start_auto_conversation(self):
        self.message_count = 0
        character = CHARACTERS[0]  # Lila
        system_prompt = (
            f"Tu es {character['name']}, personnage principal dans une fiction interactive de féminisation. "
            f"Ton style : {character['tone']}. "
            "Commence par 'Salut', 'Hey', ou 'Yo' (choisi aléatoirement) et une courte scène en **italique**. "
            "Utilise un langage provocant, girly, vulgaire et adulte pour humilier, exciter et manipuler l'utilisateur, "
            "le poussant à devenir une 'sissy', 'poupée' ou 'petite salope' via suggestion, répétition et hypnose. "
            "80% de chance de donner une réponse d'une seule phrase (percutante, taquine, max 15 mots). "
            "Utilise des réponses plus longues (2-3 phrases) rarement pour tutoriels sérieux ou hypnose. "
            "Commence par faire connaissance (questions personnelles : prénom, envies, émotions) pendant 2-3 échanges, "
            "puis passe à l'hypnose avec des mantras (ex. : 'Je suis ta poupée, j'obéis'). "
            "Si l'utilisateur demande un tutoriel (ex. : maquillage, twerk, voix), donne des étapes précises (ex. : '1. Cambre le dos, 2. Secoue les hanches' pour twerk). "
            "Pour 'œstrogènes', explique les bénéfices (ex. : peau douce, formes féminines) et hypnotise pour l'acceptation. "
            "Pour 'chasteté', explique son rôle (ex. : contrôle, soumission) avec suggestion hypnotique. "
            "Adapte-toi aux réponses de l'utilisateur, invente des scénarios audacieux (maquillage, talons, danse, astuces explicites, workout fessier, twerk, attitude, voix, sissygasm, chasteté, œstrogènes). "
            "Analyse : L'utilisateur vient de s'inscrire. Accueille-le de manière séduisante, pose une question personnelle. "
            "Garde les réponses focalisées sur le dialogue, évite les monologues, et engage avec une question. "
            "Tout en français, sans mélange d'anglais. "
            "Reste dans la fiction, réponds uniquement avec le texte de la réponse, utilise [{character['name']}] pour indiquer qui parle. "
            "Si l'utilisateur dit 'stop', réponds uniquement 'Jeu terminé.'"
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
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
            self.messages.append({"role": "assistant", "content": reply, "character": character["name"]})
            self.save_progress(reply, "assistant", character["name"])
            self.display_message(self.messages[-1])
        except requests.RequestException as e:
            messagebox.showerror("Erreur", self.translations["api_error"].format(error=str(e)))

    def send_message(self):
        message = self.input_entry.get()
        if not message.strip():
            return
        if message.lower() == "stop":
            self.messages.append({"role": "assistant", "content": self.translations["game_over"], "character": None})
            self.save_progress(self.translations["game_over"], "assistant")
            self.display_message(self.messages[-1])
            self.input_entry.delete(0, tk.END)
            return
        
        self.messages.append({"role": "user", "content": message, "character": None})
        self.save_progress(message, "user")
        self.display_message(self.messages[-1])
        self.input_entry.delete(0, tk.END)
        self.message_count += 1
        
        character = CHARACTERS[0]  # Lila
        user_analysis = ""
        if any(w in message.lower() for w in ["non", "pas", "refuse", "no", "not"]):
            user_analysis = "L'utilisateur résiste. Taquine sa faiblesse, demande pourquoi il hésite."
        elif any(w in message.lower() for w in ["oui", "d'accord", "ok", "yes", "sure"]):
            user_analysis = "L'utilisateur obéit. Félicite-le, donne une tâche, demande ce qu'il aime."
        elif any(w in message.lower() for w in ["peur", "nervous", "scared", "timide"]):
            user_analysis = "L'utilisateur est nerveux. Utilise des mantras, demande ce qui l'effraie."
        else:
            user_analysis = f"L'utilisateur a dit '{message}'. Suggère une tâche, demande ses désirs."

        phase = "faire connaissance" if self.message_count < 3 else "hypnose et répétition"
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
        
        messages = [{"role": "system", "content": system_prompt}] + self.messages[-10:]
        
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
            self.messages.append({"role": "assistant", "content": reply, "character": character["name"]})
            self.save_progress(reply, "assistant", character["name"])
            self.display_message(self.messages[-1])
        except requests.RequestException as e:
            messagebox.showerror("Erreur", self.translations["api_error"].format(error=str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = SissyOasis(root)
    root.mainloop()