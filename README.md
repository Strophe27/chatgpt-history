# 📌 Projet : Lecteur d'Historique ChatGPT

## **🔍 Besoin & Contexte**

L'objectif de ce projet est de créer une **interface complète de gestion des historiques de conversations ChatGPT**. Le projet repose sur l'importation, le stockage et la visualisation des conversations extraites depuis un fichier JSON généré par ChatGPT.

Le besoin principal est de **faciliter l'exploration et l'organisation** de ces conversations grâce à un système permettant :

- L'archivage et le filtrage des conversations.
- La navigation par dossiers et agents.
- Une interface ergonomique pour afficher et parcourir les échanges.

## **📂 Organisation du Dépôt**

### **1️⃣ API & Importation des Données**  *(Dossier : ****`API_Import_tests`****)*

Ce dossier contient tous les scripts Python liés à l'importation des données et à l'API permettant de récupérer et manipuler les conversations.

- `api.py` → API FastAPI fonctionnelle pour récupérer et gérer les conversations.
- `import_db.py` → Script principal d'importation des conversations JSON vers SQLite.
- `init_db.py` → Initialisation de la base de données SQLite.
- `extract_gizmo_ids.py` → Script pour récupérer les identifiants des agents.
- `generate_graphs.py` → Génération de statistiques sur l'utilisation de ChatGPT.
- `TEST_import_affichage_terminal.py` & `TEST_compte_nbre_conversations.py` → Tests d'import et d'affichage pour vérifier la structure du JSON initial.

### **2️⃣ Frontend - Interface Utilisateur** *(Dossier : ****`src`**** & ****`public`****)*

L'interface web est développée en **React** et se compose de plusieurs composants :

- `ConversationList.js` → Affichage des conversations disponibles.
- `ConversationDetail.js` → Affichage détaillé d'une conversation.
- `Sidebar.js` → Gestion des dossiers et filtres.
- `App.js` → Point d'entrée principal de l'application React.

### **3️⃣ Données & Configuration**

- `chatgpt_history.db` → Base de données SQLite contenant les conversations importées.
- `conversations.json` → Fichier JSON brut contenant les conversations extraites de ChatGPT.
- `.gitignore` → Fichiers et dossiers ignorés dans le dépôt (ex. `node_modules/`, `.env`).
- `package.json` → Dépendances et scripts pour le projet React.

## **📌 État de la Version Actuelle**

✅ **Importation et stockage des conversations** dans SQLite.
✅ **API opérationnelle** via FastAPI pour récupérer les conversations et les afficher.
✅ **Interface React fonctionnelle** avec affichage des conversations.
✅ **Système de dossiers** permettant de regrouper les conversations.
✅ **Archivage et filtres** pour trier les conversations.

🚧 **Problèmes en cours :**

- L'interface n'est pas encore totalement optimisée visuellement.
- Amélioration du CSS et de l'affichage des conversations.
- Organisation plus claire des fichiers et tests unitaires.

## **📜 Attentes pour la Suite (Verbatim du Cahier des Charges)**

1. **Améliorer l'affichage de l'interface utilisateur**

   - Sidebar fixe en haut avec les dossiers (zone fixe).
   - Liste des conversations en dessous avec ascenseur (zone mobile).
   - Affichage détaillé des conversations dans une zone mobile distincte.

2. **Intégrer les interactions utilisateur**

   - Ajout d'un système de **favoris** et **classement par tags**.
   - Possibilité de **modifier les noms des agents** directement depuis l'interface.
   - **Boutons d'actions** clairs pour archiver, éditer ou supprimer des conversations.

3. **Optimisation des performances & UX**

   - Correction des bugs d'affichage et du style CSS.
   - Chargement rapide des conversations sans ralentissement.
   - Ajout d’une **recherche avancée** (par mots-clés, date, etc.).

## **📢 Contribuer & Contact**

Toute contribution est la bienvenue !

- Clonez le repo : `git clone https://github.com/strophe27/chatgpt-history.git`
- Installez les dépendances backend : `pip install -r requirements.txt`
- Lancez le backend : `uvicorn api:app --reload`
- Installez les dépendances frontend : `npm install`
- Lancez l'interface React : `npm start`

🚀 **Prochaine étape : améliorer l'affichage et ajouter les interactions utilisateur !**

