import re
import json
import time
import string
import random
import secrets
import hashlib
import requests
from requests.adapters import HTTPAdapter
from commons.helpers.load_doten import Dotenv
from commons.instances.instances import logger
from requests.packages.urllib3.util.retry import Retry


def get_empty_keys(data: dict) -> list:
    empty_keys = []
    for key, value in data.items():
        if not value:
            empty_keys.append(key)
    return empty_keys


def validate_password(password: str) -> bool:
    if len(password) < 6:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
        
    if not re.search(r'[a-z]', password):
        return False
        
    if not re.search(r'[0-9]', password):
        return False
    
    special_characters = string.punctuation
    if not any(char in special_characters for char in password):
        return False
        
    return True


def generate_password(length=8):
    characters = string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def geolocate_ip(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        if response.status_code == 200:
            location_data = response.json()
            return f"{location_data.get('city', '')}, {location_data.get('region', '')}, {location_data.get('country_name', '')}"
        else:
            return ip
    except:
        return ip


def check_mail(email):
    url = "https://mailcheck.p.rapidapi.com/"
    querystring = {"email": email}
    headers = {
        'x-rapidapi-host': Dotenv.X_RAPID_API_HOST,
        'x-rapidapi-key': Dotenv.X_RAPID_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            return {
                "disposable": data.get("disposable", False),
                "reason": data.get("text", "")
            }
        else:
            return {
                "disposable": None,
                "reason": f"Erreur API : {response.status_code}"
            }
    except Exception as e:
        return {
            "disposable": None,
            "reason": str(e)
        }


def parse_and_validate_working_hours(working_hours_raw):
    try:
        working_hours = json.loads(working_hours_raw)
    except json.JSONDecodeError:
        return False, "Format des horaires invalide. Utilisez un JSON valide."

    valid_days = {str(i) for i in range(0, 7)}
    for day, slots in working_hours.items():
        if day not in valid_days:
            return False, f"Jour invalide '{day}'. Utilisez 0 (dimanche) à 6 (samedi)."

        if not isinstance(slots, list):
            return False, f"Les horaires pour le jour {day} doivent être une liste."

        for slot in slots:
            if not isinstance(slot, str):
                return False, f"Chaque horaire du jour {day} doit être une chaîne."
            
            if not re.match(r"^\d{2}:\d{2}-\d{2}:\d{2}$", slot):
                return False, f"Horaire invalide '{slot}' pour le jour {day}. Format attendu: HH:MM-HH:MM."

    return working_hours


def is_valid_email(email: str) -> bool:
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email.strip()))


def generate_strong_password(email):
    timestamp = int(time.time() * 1000)
        
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    to_hash = salt[:4] + email.lower().strip() + str(timestamp) + salt[4:]
        
    hash_obj = hashlib.sha256(to_hash.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
        
    charset = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    password = ''
    for i in range(0, len(hash_hex), 2):
        byte_val = int(hash_hex[i:i+2], 16)
        password += charset[byte_val % len(charset)]
        
    while len(password) < 16:
        password += random.choice(charset)
        
    return password[:16]


def validate_ifu(ifu: str, country_code: str = "BJ") -> tuple[bool, str]:
    if not ifu:
        return False, "Le champ IFU est requis."

    ifu = ifu.strip().upper()

    if not re.match(r'^[A-Z0-9]+$', ifu):
        return False, "L'IFU ne doit contenir que des lettres et chiffres, sans espace."

    if country_code.upper() == "BJ":
        if not re.match(r'^\d{13}$', ifu):
            return False, "Format IFU Bénin invalide (13 chiffres attendus)."

        try:
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('https://', adapter)

            response = session.get(f"https://ifubackend.impots.bj/api/default/searchByIFU/{ifu}", timeout=20)
            response.raise_for_status()
            data = response.json()
            if all(c in data.keys() for c in ("success", "message")):
                return data.get("success"), data.get("message")
            else:
                raise Exception()
        except Exception as e:
            logger.error(f"Error validating IFU : {e}")
            return False, "IFU soumis invalide."

    elif country_code.upper() == "CI":
        if not re.match(r'^CI\d{10}[A-Z]$', ifu):
            return False, "Format IFU Côte d’Ivoire invalide (ex: CI1234567890A)."
        return True, "IFU Côte d’Ivoire valide."

    elif country_code.upper() == "TG":
        if not re.match(r'^\d{11}$', ifu):
            return False, "Format IFU Togo invalide (11 chiffres attendus)."
        return True, "IFU Togo valide."

    elif country_code.upper() == "NE":
        if not re.match(r'^\d{14}$', ifu):
            return False, "Format IFU Niger invalide (14 chiffres attendus)."
        return True, "IFU Niger valide."

    return False, f"Aucune validation définie pour le pays '{country_code}'."


def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ["true", "1"]:
            return True
        elif value_lower in ["false", "0"]:
            return False
    if isinstance(value, int):
        if value == 1:
            return True
        elif value == 0:
            return False
    return False


def validate_username(username: str) -> tuple[bool, str]:
    if not username:
        return False, "Le nom d'utilisateur est requis."

    username = username.strip()

    if len(username) < 3:
        return False, "Le nom d'utilisateur doit contenir au moins 3 caractères."

    if not re.match(r'^[A-Za-z0-9_]+$', username):
        return False, "Le nom d'utilisateur ne doit contenir que des lettres, chiffres et underscores (_)."

    return True, "Nom d'utilisateur valide."
