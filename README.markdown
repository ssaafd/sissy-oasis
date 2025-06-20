# Sissy Oasis

**Sissy Oasis** est un jeu interactif en Python avec une interface Tkinter, conçu pour une expérience de fiction immersive. Le jeu propose un chat avec Lila, une amie perverse et bimbo, qui guide l'utilisateur à travers des dialogues provocants, des tutoriels sérieux, et des sessions d'hypnose.

**Attention** : Contenu explicite avec thèmes d’humiliation/féminisation. Destiné à un public adulte consenti.

## Prérequis

- Python 3.8+
- Tkinter (inclus avec Python, sur Linux : `sudo apt-get install python3-tk`)
- Bibliothèque `requests` : `pip install requests`
- Clé API xAI (obtenez-la via https://api.x.ai/docs)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/your-username/sissy-oasis.git
   cd sissy-oasis
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Vérifiez la clé API xAI dans `sissy_oasis.py` :
   ```python
   API_KEY = "xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW"
   ```

4. Lancez le jeu :
   ```bash
   python sissy_oasis.py
   ```

## Utilisation

1. Choisissez une langue (français, anglais, espagnol).
2. Entrez le mot de passe général : "1245".
3. Inscrivez-vous ou connectez-vous avec un prénom (ex. : "Chloé") et un mot de passe.
4. Interagissez avec Lila via des messages tapés (appuyez sur "Envoyer" ou Entrée).
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
Vous: Apprends-moi à twerker
*Une salle de danse, miroirs partout.*
Salut, ma belle ! 1. Cambre le dos, 2. Secoue les hanches. Tu twerkes ? [Lila] (rose foncé)
```

## Fonctionnalités

- **Personnage** : Lila, amie perverse et bimbo (rose foncé #C71585).
- **Dialogues** : 80% une phrase (max 15 mots), tutoriels/hypnose rares (2-3 phrases).
- **Faire connaissance** : 2-3 échanges personnels.
- **Hypnose/répétition** : Mantras après 2-3 messages (ex. : "Je suis ta poupée").
- **Tutoriels sérieux** : Sur demande (ex. : twerk : "1. Cambre le dos, 2. Secoue les hanches").
- **Œstrogènes** : Bénéfices (ex. : peau douce) + hypnose.
- **Chasteté** : Rôle (ex. : soumission) + suggestion.
- **Design** : Interface pastel (rose #ffeacc, lavande #f3e5f5, turquoise #00ced1), emojis (💕, 💋).
- **Sauvegarde** : SQLite (sissy_oasis.db).

## Résolution des problèmes

- **Erreur 400 API** : Vérifiez la clé API dans `sissy_oasis.py` ou consultez https://api.x.ai/docs. Testez avec Postman :
  ```bash
  curl -X POST https://api.x.ai/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer xai-brO1cDAipzQkNEyTEQRW7lsL1vqGkLc9yBkjYXgws6nQf2Uvn4lICPrapGw70krwXDH1D2zmsJE8jOqW" -d '{"model": "grok-3-latest", "messages": [{"role": "user", "content": "Test"}]}'
  ```
- **Tkinter manquant** : Installez Tkinter (Linux : `sudo apt-get install python3-tk`).
- **SQLite** : Assurez-vous que `sissy_oasis.db` est accessible.
- **Dialogues longs** : Contactez-moi pour ajuster le prompt.

## Personnalisation

Pour modifier :
- **Tutoriels** : Ajoutez des scénarios dans `system_prompt`.
- **Hypnose** : Augmentez les mantras dans `system_prompt`.
- **Design** : Changez les couleurs/emojis dans le code.

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