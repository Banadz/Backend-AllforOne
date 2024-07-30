from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from django.http import request
from fastapi import Request
import sqlite3


from pydantic import BaseModel

# from ipware import get_client_ip

import math

from fastapi.responses import JSONResponse
from django.http import JsonResponse
from fastapi.middleware.cors import CORSMiddleware
# from google.cloud import texttospeech
# from fastapi.responses import StreamingResponse
# import io

import datetime
import os
import requests

app = FastAPI()

# Configurer les en-têtes CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vous pouvez spécifier les domaines autorisés
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/")
def read_api():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/message")
async def get_message():
    return {"message": "Hello from FastAPI!"}

@app.post('/data')
async def receive_data(data: dict):
    # Vous pouvez maintenant utiliser les données reçues dans 'data'
    print(data['test'])
    # Vous pouvez également effectuer des opérations sur les données ici
    return {"message": "Données reçues avec succès"}

# from fullBack.models import Agent
from django.conf import settings

from fullBack.fonction import Query
from fullBack.fonction import generate_token
from fullBack.fonction import get_all_info_user
# from fullBack.fonction import Requery
import json
from fastapi import Form

from pydantic import BaseModel
# from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post('/tologin')
# def receive_login(email: str = Form('email'), password: str = Form('password')):
def receive_login(login_data: LoginRequest):
    email = login_data.email
    password = login_data.password
    if email and '@' in email and '.' in email:
        row = Query("SELECT * FROM `User` WHERE email = %s", (email,))
        if row:
            eff = row[0][0]
        else:
            eff = 0
        if eff != 0 :
            rowi = Query("SELECT COUNT(*) FROM User WHERE email = %s and password = %s", (email, password))
            if row:
                count = rowi[0][0]
            else:
                count = 0
            if count !=0 :
                bigdata = generate_token(email, password)
                # _token = bigdata[0]
                # userInfo = bigdata[1]
                res = {"success":bigdata}
                return JsonResponse(res)
            else:
                return JsonResponse({'error': 'Le mot de passe est incorrect'}, status=404)
        else:
            return JsonResponse({'error': 'Aucun e-mail correspondant'}, status=404)

    else:
        return JsonResponse({'error': 'L\'e-mail est incorrectement formaté', "email":email}, status=400)
    # return JsonResponse({'data':row})
    

    # objets = Agent.objects.all()
    # from django.contrib.auth.models import User
    # from django.contrib.auth import authenticate

    # user = authenticate(username=data['nomUtilisateur'], password=data['motDePasse'])

    # if user is not None:
    #     return {"rapport":"Authentification réussie pour l'utilisateur:"}
    # else:
    #     # L'authentification a échoué
    # return {"rapport":"Authentification échouée"}

# Accédez à la clé API à partir de la variable d'environnement

cle_api_weatherstack = os.environ.get("WEATHERSTACK_API_KEY")
@app.get("/obtenir_meteo")
async def get_meteo():

    url = f'http://api.weatherstack.com/current?access_key=ad5e07b74e2737f4d76709418692f4e5&query=Madagascar'
    reponse= requests.get(url)
    response=reponse.json()

    return {"response":response}

# Approximation de capacité de production à partir
# des données météorologique

from pydantic import BaseModel
# Poids constants
POIDS_RADIATION = 0.6
POIDS_COUVERTURE_NUAGEUSE = 0.3
POIDS_TEMPERATURE = 0.3
POIDS_VITESSE_VENT = 0.1
POIDS_HUMIDITE = 0.1
    


@app.get("/estimationProductionSolaire")
async def estimation_production_solaire():
    url = f'http://api.weatherstack.com/current?access_key=ad5e07b74e2737f4d76709418692f4e5&query=Madagascar'
    radiation: float
    couverture_nuageuse: float
    temperature: float
    vitesse_vent: float
    humidite: float
    answer=requests.get(url)
    meteo=answer.json()
    heure_locale = meteo["current"]["observation_time"]
    latitude = float(meteo["location"]["lat"])
    couverture_nuageuse = meteo["current"]["cloudcover"]
    temperature = meteo["current"]["temperature"]
    pression = meteo["current"]["pressure"]

    # couverture_nuageuse = 2
    # temperature = 35
    # pression = 41

    def determiner_saison(heure_locale):
        # Vérifier si l'heure_locale contient au moins deux éléments
        elements = heure_locale.split("-")
        if len(elements) >= 2:
            mois = int(elements[1])  # Extrait le mois à partir de l'heure locale
            if 3 <= mois <= 5:
                return "printemps"
            elif 6 <= mois <= 8:
                return "été"
            elif 9 <= mois <= 11:
                return "automne"
            else:
                return "hiver"
        else:
            return "Mois non valide"  # Gérer le cas où l'heure_locale ne contient pas suffisamment d'éléments
    saison = determiner_saison(heure_locale)
    def estimer_heure_lever_soleil(saison, latitude):
    # Approximation de l'heure du lever du soleil en fonction de la saison et de la latitude.
    # Vous devrez remplacer ces approximations par des calculs précis.
        if saison == "été":
            if latitude > 0:
                heure_lever_soleil = "05:30 AM"
            else:
                heure_lever_soleil = "06:30 AM"
        else:
            heure_lever_soleil = "07:00 AM"
        return heure_lever_soleil

    def estimer_heure_coucher_soleil(saison, latitude):
        # Approximation de l'heure du coucher du soleil en fonction de la saison et de la latitude.
        # Vous devrez remplacer ces approximations par des calculs précis.
        if saison == "été":
            if latitude > 0:
                heure_coucher_soleil = "08:00 PM"
            else:
                heure_coucher_soleil = "07:30 PM"
        else:
            heure_coucher_soleil = "06:30 PM"
        return heure_coucher_soleil

    def estimer_angle_incidence(latitude, saison):
        # Approximation de l'angle d'incidence en fonction de la latitude et de la saison.
        # Vous devrez remplacer cette approximation par une formule plus précise.

        # Convertir la latitude en radians
        latitude_rad = math.radians(latitude)

        # Définir une approximation de l'angle d'incidence en radians en fonction de la saison
        if saison == "été":
            angle_incidence_rad = math.radians(45)  # Exemple : 45 degrés pour l'été
        else:
            angle_incidence_rad = math.radians(30)  # Exemple : 30 degrés pour l'hiver

        # Si la latitude est négative (hémisphère sud), ajuster l'angle d'incidence
        if latitude < 0:
            angle_incidence_rad = -angle_incidence_rad

        # Convertir l'angle d'incidence en degrés pour la sortie
        angle_incidence_deg = math.degrees(angle_incidence_rad)

        return angle_incidence_deg


    angle_incidences = estimer_angle_incidence(latitude, saison)

    def estimer_radiation_potentielle(angle_incidences, temperature, pression):
        # Approximation de la radiation solaire potentielle en fonction de l'angle d'incidence, de la température et de la pression.
        # Vous devrez remplacer cette approximation par des formules plus précises.

        # Coefficients de correction
        coeff_angle = 0.7  # Exemple : coefficient d'angle
        coeff_temperature = 0.8  # Exemple : coefficient de température
        coeff_pression = 1.2  # Exemple : coefficient de pression

        # Formule simplifiée pour l'estimation de la radiation
        radiation_potentielle = coeff_angle * angle_incidences + coeff_temperature * temperature - coeff_pression * pression

        # Assurez-vous que la radiation est toujours positive
        radiation_potentielle = max(0, radiation_potentielle)

        return radiation_potentielle

    def estimer_radiation_solaire(latitude, saison, couverture_nuageuse, heure_locale, temperature, pression):
    # Déterminez si c'est le jour (soleil levé).
    
        est_jour = heure_locale >= estimer_heure_lever_soleil(saison, latitude) and heure_locale <= estimer_heure_coucher_soleil(saison, latitude)

        if est_jour:
            # Estimez l'angle d'incidence du soleil en degrés.
            angle_incidence = estimer_angle_incidence(latitude, saison)

            # Estimez la radiation solaire potentielle en watts par mètre carré (W/m²).
            radiation_potentielle = estimer_radiation_potentielle(angle_incidence, temperature, pression)

            # Réduisez la radiation due à la couverture nuageuse.
            radiation_reduite = radiation_potentielle * (1 - couverture_nuageuse)

            return radiation_reduite
        else:
            return 0  # La radiation solaire est nulle la nuit.
    
    radiation = estimer_radiation_solaire(latitude, saison, couverture_nuageuse, heure_locale, temperature, pression)
    


    # Utilisez les poids constants pour calculer l'estimation de la production d'énergie solaire
    score_radiation = (radiation- 0) / (1000 - 0)
    score_couverture_nuageuse = couverture_nuageuse / 100
    score_temperature = (temperature - (-20)) / (40 - (-20))
    score_vitesse_vent = (meteo["current"]["wind_speed"] - 0) / (30 - 0)
    score_humidite = (meteo["current"]["humidity"] - 0) / (100 - 0)

    lever_soleil = estimer_heure_lever_soleil(saison, latitude)
    coucher_soleil = estimer_heure_coucher_soleil(saison, latitude)
    radiation_potenteille = estimer_radiation_potentielle(angle_incidences, temperature, pression)
    radiation_solaire = estimer_radiation_solaire(latitude, saison, couverture_nuageuse, heure_locale, temperature, pression)
    

    estimation = (
        POIDS_RADIATION * score_radiation +
        POIDS_COUVERTURE_NUAGEUSE * (1 - score_couverture_nuageuse) +
        POIDS_TEMPERATURE * score_temperature +
        POIDS_VITESSE_VENT * score_vitesse_vent +
        POIDS_HUMIDITE * (1 - score_humidite)
    ) * 80  # 80% de la capacité maximale
    production_estimee = round(estimation,2)
    angle_incidence = round(angle_incidences,2)
    bigData = {
        "production_estimee": production_estimee,
        "saison": saison,
        "radiation": radiation,
        "lever_soleil": lever_soleil,
        "coucher_soleil": coucher_soleil,
        "radiation_potentielle": radiation_potenteille,
        "angle_incidence": angle_incidence,
        "radiation_solaire": radiation_solaire,
        "temperature": temperature,
    }

    return {"bigData":bigData}
# class RequestModel(BaseModel):
#     request: str 

@app.get("/geoLocalisation")
async def localisation(request):
    client_ip, is_routable = request.client.host  # Obtenez l'adresse IP du client depuis la requête

    if client_ip is not None:
        # Utilisez l'adresse IP pour interroger l'API externe ou effectuer d'autres opérations
        url = f'http://ip-api.com/json/{client_ip}'
        response = requests.get(url)
        position = response.json()

        response_data = {
            "ip": client_ip,
            "country": position.get("country", "Pays de l'utilisateur"),
            "region": position.get("region", "Région de l'utilisateur"),
            "city": position.get("city", "Ville de l'utilisateur"),
            "latitude": position.get("lat", 0.0),
            "longitude": position.get("lon", 0.0)
        }
    else:
        response_data = {
            "error": "Impossible de récupérer l'adresse IP de l'utilisateur."
        }

    return response_data
    


# ============================================================== TEXT To SPEECH  =====================================================

# @app.get("/texteToSpeech")
# async def convert_text_to_speech(text):
#     client = texttospeech.TextToSpeechClient()
#     synthesis_input = texttospeech.SynthesisInput(text=text)
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="fr-FR",
#         name="fr-FR-Wavenet-A",
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE 
#     )
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3  
#     )

#     response = client.synthesize_speech(
#         input=synthesis_input, voice=voice, audio_config=audio_config
#     )
#     audio_content = response.audio_content

#     return StreamingResponse(io.BytesIO(audio_content), media_type="audio/mpeg")

# ======================================= BOT ===================================================
from fullBack.chatBot import testOpenAI
@app.get("/bot")
def tester():
    res = testOpenAI()
    return JsonResponse(res)
