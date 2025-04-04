# Documentation des Endpoints de Profil

## Vue d'ensemble

Ce document décrit les endpoints liés aux profils utilisateurs dans l'API. Ces endpoints permettent de gérer les profils utilisateurs, y compris la récupération des profils individuels, la liste des profils, et les fonctionnalités de suivi.

## Endpoints

### 1. Récupérer la liste des profils

```http
GET /profiles
```

#### Description

Récupère la liste de tous les profils utilisateurs. Si l'utilisateur est authentifié, l'état "following" est correctement défini pour chaque profil.

#### Paramètres

- Aucun paramètre requis
- Authentification optionnelle (via header Authorization)

#### Réponse

```json
{
  "profiles": [
    {
      "username": "string",
      "bio": "string | null",
      "image": "string | null",
      "following": boolean
    }
  ]
}
```

#### Exemple de réponse

```json
{
  "profiles": [
    {
      "username": "john_doe",
      "bio": "Software developer",
      "image": "https://example.com/image.jpg",
      "following": false
    },
    {
      "username": "jane_doe",
      "bio": "Product manager",
      "image": "https://example.com/image2.jpg",
      "following": true
    }
  ]
}
```

### 2. Récupérer un profil spécifique

```http
GET /profiles/{username}
```

#### Description

Récupère les informations d'un profil utilisateur spécifique.

#### Paramètres

- `username` (path): Le nom d'utilisateur du profil à récupérer
- Authentification optionnelle (via header Authorization)

#### Réponse

```json
{
  "profile": {
    "username": "string",
    "bio": "string | null",
    "image": "string | null",
    "following": boolean
  }
}
```

### 3. Suivre un utilisateur

```http
POST /profiles/{username}/follow
```

#### Description

Permet à l'utilisateur authentifié de suivre un autre utilisateur.

#### Paramètres

- `username` (path): Le nom d'utilisateur à suivre
- Authentification requise (via header Authorization)

#### Réponse

```json
{
  "profile": {
    "username": "string",
    "bio": "string | null",
    "image": "string | null",
    "following": true
  }
}
```

### 4. Ne plus suivre un utilisateur

```http
DELETE /profiles/{username}/follow
```

#### Description

Permet à l'utilisateur authentifié de ne plus suivre un autre utilisateur.

#### Paramètres

- `username` (path): Le nom d'utilisateur à ne plus suivre
- Authentification requise (via header Authorization)

#### Réponse

```json
{
  "profile": {
    "username": "string",
    "bio": "string | null",
    "image": "string | null",
    "following": false
  }
}
```

## Tests Unitaires

Les tests unitaires couvrent les scénarios suivants :

1. Récupération de la liste des profils sans authentification
2. Récupération de la liste des profils avec authentification
3. Vérification de la structure des profils retournés
4. Vérification de l'état "following" pour les utilisateurs authentifiés

## Structure du Code

- `src/endpoints/profile.py`: Contient les routes et la logique des endpoints
- `src/core/user.py`: Contient les fonctions de base pour interagir avec les utilisateurs
- `src/schemas/user.py`: Définit les modèles de données pour les réponses
- `tests/test_profile.py`: Contient les tests unitaires

## Notes d'Implémentation

- L'état "following" est calculé dynamiquement en fonction de l'utilisateur authentifié
- Les profils sont stockés dans une base de données MongoDB via ODMantic
- La pagination n'est pas implémentée pour la liste des profils (à considérer pour une version future)
