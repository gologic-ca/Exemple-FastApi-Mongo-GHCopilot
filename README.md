# ![Formation GoLogic Example de Projet](Gologic.png)

## Pré-requis pour exemple de projet 

Nous sommes ravis d'explorer GitHub Copilot avec vous à travers des exemples pratiques. Pour assurer le bon déroulement, veuillez préparer votre poste de travail de la manière suivante :

- Installer un environnement de développement (choisissez l'une des options suivantes) :
  - **Visual Studio Code** : [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

- [Installer Docker](https://docs.docker.com/engine/install/) (Pour l'entité local de MongoDB)

- Installer Python ( >= Version 3.11) [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Assurez-vous que les variables dans votre système sont bien configurés
    - Tapez "View Advanced System Settings" dans la barre de recherche
    - Dans "Advanced", cliquez "Environment Variables" en bas à droit
    - Sélectionnez "Path", clicquez "Edit..." (ou double-cliquez "Path")
    - ***Cliquez "New" et insérez le path vers votre version de python*** 
    - Pour moi c'est: `C:\Users\SpencerHandfield\AppData\Local\Programs\Python\Python313` et `C:\Users\SpencerHandfield\AppData\Local\Programs\Python\Python313\Scripts`
    - Vérifiez si ça bien fonctionner en tapant `py --version` dans le terminal

- Installer uv [https://docs.astral.sh/uv/getting-started/installation/#standalone-installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
    - **Dans Terminal** Dans VSCode, Ouvrez un nouveau terminal et roulez la commande `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

## Démarrer l'application

### Avec Visual Studio Code :
- Ouvrir VSCode et ouvrir une nouvelle fenêtre (Ctrl+Shift+N).
- Dans l'accueil, cliquer sur "Clone Git Repository...", entrer l'URL de ce dépôt (à savoir : [https://github.com/gologic-ca/Exemple-FastApi-Mongo-GHCopilot.git](https://github.com/gologic-ca/Exemple-FastApi-Mongo-GHCopilot.git)) et confirmer en cliquant sur "Clone from the URL". Cliquer sur "Open".
- Une fois le projet ouvert, ouvrir un nouveau terminal (Shift+Ctrl+\`). Exécuter les commandes :
`uv sync`, `source .venv/Scripts/activate` et finalement `uvicorn --app-dir ./src/ api:app`

Félicitations l'application devrait bien être parti !

### :bulb: Scripts individuels

- Start the MongoDB instance `./scripts/start-mongo.sh`
- Stop the MongoDB instance `./scripts/stop-mongo.sh`
- Start the FastAPI server `./scripts/start.sh`
- Format the code `./scripts/format.sh`
- Manually run the linter `./scripts/lint.sh`
- Manually run the tests `./scripts/test.sh`
