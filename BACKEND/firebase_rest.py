
import requests

FIREBASE_CONFIG = {} # Enter your firebase config here


class FirebaseREST:
    def __init__(self):
        self.api_key = FIREBASE_CONFIG["apiKey"]
        self.database_url = FIREBASE_CONFIG["databaseURL"]

    def signup(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        res = requests.post(url, json=payload)

        if "error" in res.json():
            raise requests.exceptions.HTTPError(response=res)

        return res.json()

    def signin(self, email, password):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        res = requests.post(url, json=payload)

        if "error" in res.json():
            raise requests.exceptions.HTTPError(response=res)

        return res.json()

    def refresh_token(self, refresh_token):
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        res = requests.post(url, data=payload)
        
        if "error" in res.json():
            raise requests.exceptions.HTTPError(response=res)

        return res.json()

    def put_data(self, id_token, path, data):
        url = f"{self.database_url}/{path}.json?auth={id_token}"
        res = requests.put(url, json=data)
        
        if "error" in res.json():
            raise requests.exceptions.HTTPError(response=res)

        return res.json()


    def get_data(self, id_token: str, path: str):
        url = f"{self.database_url}/{path}.json?auth={id_token}"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()  # raises HTTPError for bad status

            data = res.json()
            if data is None:
                return {}  # Firebase path exists but has no content

            if isinstance(data, dict) and "error" in data:
                raise Exception(f"Firebase error: {data['error']}")

            return data

        except requests.exceptions.RequestException as e:
            print(f"[FIREBASE ERROR]: {e}")
            return {}

    def send_password_reset_email(self, email):
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={self.api_key}"
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": email
        }
        requests.post(url, json=payload)

    def get_firebase_error_msg(self, error_code):
        errors = {
            "EMAIL_NOT_FOUND": "No user found with that email.",
            "INVALID_PASSWORD": "Incorrect password.",
            "INVALID_LOGIN_CREDENTIALS": "Incorrect Email or Password.",
            "USER_DISABLED": "This account has been disabled.",
            "INVALID_EMAIL": "Invalid email address format.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many login attempts. Try again later.",
            "EMAIL_EXISTS": "An account with this email already exists.",
            "OPERATION_NOT_ALLOWED": "Password sign-in is disabled for this project.",
            "WEAK_PASSWORD": "Password is too weak. It should be at least 6 characters."
        }

        for key in errors:
            if key in error_code:
                return errors[key]

        return f"Error: {error_code}"
