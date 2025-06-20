# Sissy Oasis (Web App)

**Sissy Oasis** est une application web Python basée sur Flask, conçue pour une expérience de fiction interactive immersive. L'application propose un chat avec Lila, une amie perverse et bimbo, qui guide l'utilisateur à travers des dialogues provocants, des tutoriels sérieux, et des sessions d'hypnose.

**Attention** : Contenu explicite avec thèmes d’humiliation/féminisation. Destiné à un public adulte consenti.

## Prérequis

- Python 3.8+
- Clé API xAI (obtenez-la via https://api.x.ai/docs)
- Git (https://git-scm.com/download/win)

## Installation locale

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/your-username/sissy-oasis.git
   cd sissy-oasis
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Vérifiez la clé API xAI dans `app.py` :
   ```python
   API_KEY = "xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW"
   ```

4. Lancez l'application :
   ```bash
   python app.py
   ```
   - Accédez à `http://localhost:5000` dans votre navigateur.

## Déploiement sur Render

1. Poussez le dépôt sur GitHub (voir ci-dessous).
2. Connectez-vous à Render (https://render.com).
3. Créez un nouveau "Web Service" et liez votre dépôt GitHub `sissy-oasis`.
4. Configurez :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
   - **Runtime** : Python
5. Déployez et accédez à l'URL fournie par Render.

## Utilisation

1. Accédez à l'application via le navigateur.
2. Entrez le mot de passe général : "1245".
3. Inscrivez-vous ou connectez-vous avec un prénom (ex. : "Chloé") et un mot de passe.
4. Interagissez avec Lila via le chat :
   - Demandez des tutoriels (ex. : "apprends-moi à twerker" ou "parle-moi d'œstrogènes").
   - Tapez "stop" pour arrêter ("Jeu terminé.").

### Exemple

```
SISSY OASIS 💖
*Un salon rose, plumes flottantes.*
Hey, chérie ! C’est quoi ton prénom, poupée ? [Lila] (rose foncé)
Vous: Chloé
*Un sofa moelleux, parfum sucré.*
Yo, Chloé ! T’as déjà rêvé d’être ultra sexy ? [Lila] (rose foncé)
```

## Fonctionnalités

- **Personnage** : Lila, amie perverse et bimbo (rose foncé #C71585).
- **Dialogues** : 80% une phrase (max 15 mots), tutoriels/hypnose rares (2-3 phrases).
- **Faire connaissance** : 2-3 échanges personnels.
- **Hypnose/répétition** : Mantras après 2-3 messages (ex. : "Je suis ta poupée").
- **Tutoriels sérieux** : Sur demande (ex. : twerk : "1. Cambre le dos, 2. Secoue les hanches").
- **Œstrogènes** : Bénéfices (ex. : peau douce) + hypnose.
- **Chasteté** : Rôle (ex. : soumission) + suggestion.
- **Design** : Interface pastel (rose #ffeacc, lavande #f3e5f5).
- **Sauvegarde** : SQLite (sissy_oasis.db).

## Résolution des problèmes

- **Erreur 400 API** : Vérifiez la clé API dans `app.py` ou consultez https://api.x.ai/docs. Testez avec cURL :
  ```bash
  curl -X POST https://api.x.ai/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW" -d '{"model": "grok-3-latest", "messages": [{"role": "user", "content": "Test"}]}'
  ```
- **Dépôt GitHub** : Si erreur lors du push, supprimez le remote :
  ```bash
  git remote remove origin
  git remote add origin https://github.com/your-username/sissy-oasis.git
  ```

## Contribution

1. Forkez le dépôt.
2. Créez une branche : `git checkout -b feature/ton-modif`.
3. Commitez : `git commit -m "Description de la modif"`.
4. Poussez : `git push origin feature/ton-modif`.
5. Ouvrez une Pull Request.

## Licence

MIT License. Voir `LICENSE` pour détails (à ajouter si souhaité).

---

**Enjoy, ma chérie ! 💋**