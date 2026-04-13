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
        host="mysql.railway.internal",
        user="root",
        password="LCwiUHQOmgIpQrFRirDxnIPuUYZzJoTb",
        database="railway",
        port=3306 # ou le port indiqué sur Railway
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

from fastapi import Request

# --- ROUTE POUR L'INSCRIPTION ---
@app.post("/api/inscription")
async def inscription(request: Request):
    data = await request.json()
    conn = connexion_bdd()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO utilisateur (nom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s)"
        valeurs = (data['nom'], data['email'], data['mot_de_passe'], data['role'])
        
        cursor.execute(sql, valeurs)
        conn.commit()
        return {"message": "Inscription réussie ! Bienvenue."}
    except Exception as e:
        return {"erreur": f"Impossible de créer le compte : {str(e)}"}
    finally:
        cursor.close()
        conn.close()