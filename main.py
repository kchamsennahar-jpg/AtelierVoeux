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

@app.get("/")
def home():
    return {"status": "online"}

@app.post("/api/inscription")
async def inscription(request: Request):
    data = await request.json()
    try:
        conn = connexion_bdd()
        cursor = conn.cursor()
        # On s'assure que la table existe
        cursor.execute("CREATE TABLE IF NOT EXISTS utilisateur (id INT AUTO_INCREMENT PRIMARY KEY, nom VARCHAR(100), email VARCHAR(100) UNIQUE, mot_de_passe VARCHAR(255), role VARCHAR(50))")
        
        sql = "INSERT INTO utilisateur (nom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (data['nom'], data['email'], data['mot_de_passe'], data['role']))
        conn.commit()
        return {"message": "Inscrit !"}
    except Exception as e:
        return {"erreur": str(e)}
    finally:
        if 'conn' in locals(): conn.close()

@app.post("/api/connexion")
async def connexion(request: Request):
    data = await request.json()
    try:
        conn = connexion_bdd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateur WHERE email = %s AND mot_de_passe = %s", (data['email'], data['mdp']))
        user = cursor.fetchone()
        if user:
            return {"message": "OK", "role": user['role'], "nom": user['nom']}
        return {"erreur": "Identifiants incorrects"}
    except Exception as e:
        return {"erreur": str(e)}
    finally:
        if 'conn' in locals(): conn.close()