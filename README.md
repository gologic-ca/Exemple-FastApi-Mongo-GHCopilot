# ![Formation GoLogic Example de Projet](Gologic.png)

## Pré-requis pour exemple de projet 

Nous sommes ravis d'explorer GitHub Copilot avec vous à travers des exemples pratiques. Pour assurer le bon déroulement, veuillez préparer votre poste de travail de la manière suivante :

- Installer un environnement de développement (choisissez l'une des options suivantes) :
  - **Visual Studio Code** : [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

- [Installer Docker](https://docs.docker.com/engine/install/) (Pour l'instance local de MongoDB)

- Installer Python ( >= Version 3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Assurez-vous que les variables d'environements dans votre système sont bien configurés
    - Tapez "View Advanced System Settings" dans la barre de recherche
    - Dans "Advanced", cliquez "Environment Variables" en bas à droit
    - Sélectionnez "Path", clicquez "Edit..." (ou double-cliquez "Path")
    - ***Cliquez "New" et insérez le path vers votre version de python*** 
    - Pour moi c'est: `C:\Users\SpencerHandfield\AppData\Local\Programs\Python\Python313` et `C:\Users\SpencerHandfield\AppData\Local\Programs\Python\Python313\Scripts`
    - Vérifiez si ça bien fonctionner en tapant `py --version` dans le terminal

- Installer uv [https://docs.astral.sh/uv/getting-started/installation/#standalone-installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
    - **Dans Terminal** Ouvrez un nouveau terminal et roulez la commande `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

 - Installer le plugin SonarLint
    -   **Visual Studio Code** : Ouvrir VSCode, Ctrl+Shift+X, saisir "SonarQube for IDE" dans la barre de recherche, cliquer sur "Install".

## Démarrer l'application

### Avec Visual Studio Code :
- Ouvrir VSCode et ouvrir une nouvelle fenêtre (Ctrl+Shift+N).
- Dans l'accueil, cliquer sur "Clone Git Repository...", entrer l'URL de ce dépôt (à savoir : [https://github.com/gologic-ca/Exemple-FastApi-Mongo-GHCopilot.git](https://github.com/gologic-ca/Exemple-FastApi-Mongo-GHCopilot.git)) et confirmer en cliquant sur "Clone from the URL". Cliquer sur "Open".
- Une fois le projet ouvert, ouvrir un nouveau terminal (Shift+Ctrl+\`).
Exécuter la commandes :
  - `uv run uvicorn --app-dir ./src/ api:app --reload`
- Validez que l'application fonctionne en allant à `http://127.0.0.1:8000/docs` ou `localhost:8080/docs`

Félicitations l'application devrait bien être parti !

### Authorisation de l'API:

1) sur l'interface de Swagger, s'authentifier avec le endpoint `/users/login` avec les credentials suivants:
- **username**: `test@example.com`
- **password**: `testpassword`

2) Copier le token JWT qui est retourné par l'API
3) Cliquer sur le bouton en haut à droite de l'interface Swagger `Authorize`
4) Coller le token JWT dans le champ `Value` et cliquer sur `Authorize`

Tester avec le endpoint get current user pour varifier que l'authentification fonctionne correctement.

### Exécuter les tests

1) exécuter la commande suivante: 
   - `uv sync --all-groups`
2) S'assurer de créer les tests dans le dossier `tests/`
3) Si vous utiliser Visual Studio Code les tests seront disponibles dans l'onglet "Testing"
