import jwt
import requests
from jwt import PyJWTError
from jwt.algorithms import RSAAlgorithm
from commons.helpers.load_doten import Dotenv
from requests.exceptions import RequestException


def exchange_code_for_token(code: str):
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": Dotenv.OAUTH_CLIENT_ID,
        "client_secret": Dotenv.OAUTH_CLIENT_SECRET,
        "redirect_uri": Dotenv.OAUTH_REDIRECT_URI,
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()

    return response.json()


def get_access_token(refresh_token: str):
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": Dotenv.OAUTH_CLIENT_ID,
        "client_secret": Dotenv.OAUTH_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()

    data = response.json()
    access_token = data.get("access_token")
    expires_in = data.get("expires_in")

    return access_token, expires_in


def get_user_info(access_token: str):
    url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_google_public_keys():
    try:
        response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
        response.raise_for_status()
        return response.json()['keys']
    except RequestException as e:
        print(f"Erreur lors de la récupération des clés publiques : {e}")
        return None


def verify_google_id_token(id_token: str):
    try:
        unverified_header = jwt.get_unverified_header(id_token)
        if unverified_header is None:
            raise ValueError("Impossible de décoder l'en-tête du JWT.")

        kid = unverified_header.get("kid")
        if not kid:
            raise ValueError("Aucun 'kid' trouvé dans l'en-tête du JWT.")

        google_public_keys = get_google_public_keys()
        if not google_public_keys:
            raise ValueError("Aucune clé publique Google trouvée.")

        rsa_key = {}
        for key in google_public_keys:
            if key['kid'] == kid:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
                break

        if not rsa_key:
            raise ValueError(f"Aucune clé publique correspondante pour le kid {kid}")

        payload = jwt.decode(
            id_token,
            RSAAlgorithm.from_jwk(rsa_key),
            algorithms=["RS256"],
            audience=Dotenv.OAUTH_CLIENT_ID,
            issuer='https://accounts.google.com'
        )

        return payload

    except PyJWTError as e:
        raise Exception(f"Erreur lors de la vérification du JWT : {e}")
    except ValueError as e:
        raise Exception(f"Erreur de valeur : {e}")
