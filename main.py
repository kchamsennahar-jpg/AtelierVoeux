from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# Sécurité (CORS) configurée une seule fois
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connexion_bdd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="myevents_db"
    )

@app.get("/")
def accueil():
    return {"message": "Serveur Marrakech opérationnel !"}

# --- LA FAMEUSE ROUTE POUR TON SITE WEB ---
@app.get("/api/prestataire")
def get_prestataire():
    try:
        db = connexion_bdd()
        cursor = db.cursor(dictionary=True)
        # On récupère tous tes prestataires
        cursor.execute("SELECT * FROM prestataire") 
        resultats = cursor.fetchall()
        db.close()
        return resultats
    except Exception as e:
        print(f"ERREUR MYSQL : {e}")
        return {"erreur_detaillee": str(e)}

# (J'ai gardé tes autres routes en dessous pour qu'elles fonctionnent toujours)
@app.post("/creer-utilisateur")
def creer_utilisateur(id_user: int, email: str):
    # ... ton code existant
    pass
