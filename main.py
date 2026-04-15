from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connexion_bdd():
    return mysql.connector.connect(
        host="mainline.proxy.rlwy.net",
        user="root",
        password="LCwiUHQOmgIpQrFRirDxnIPuUYZzJoTb",
        database="railway",
        port=27975
    )

# Création de la table automatique au démarrage
try:
    conn = connexion_bdd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            mot_de_passe VARCHAR(255),
            role VARCHAR(50)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Erreur table: {e}")

@app.get("/")
def accueil():
    return {"status": "online", "message": "Serveur Marrakech OK"}

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
        return {"message": "Inscription réussie !"}
    except Exception as e:
        return {"erreur": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.post("/api/connexion")
async def connexion(request: Request):
    data = await request.json()
    conn = connexion_bdd()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM utilisateur WHERE email = %s AND mot_de_passe = %s"
        cursor.execute(sql, (data['email'], data['mdp']))
        user = cursor.fetchone()
        if user:
            return {"message": "OK", "role": user['role'], "nom": user['nom']}
        else:
            return {"erreur": "Identifiants incorrects"}
    finally:
        cursor.close()
        conn.close()
