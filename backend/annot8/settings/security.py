import os
import socket

from annot8.settings.base import BASE_DIR
from corsheaders.defaults import default_headers
from django.core.management.utils import get_random_secret_key
from pathlib import Path

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY_FILE = Path(os.environ.get("ANNOT8_SECRET_KEYFILE", BASE_DIR / 'secret.txt'))

if not SECRET_KEY_FILE.exists():
    with open(SECRET_KEY_FILE, "w") as f:
        f.write(get_random_secret_key())

    os.chmod(SECRET_KEY_FILE, 0o600)

SECRET_KEY = open(SECRET_KEY_FILE).read()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
CURRENT_IP = s.getsockname()[0]
s.close()

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    CURRENT_IP,
    'hemera4.inf-cv.uni-jena.de',
    'api.inf-cv.uni-jena.de',
    'annot8.dikorsch.de',
]

FRONTEND_PORT = os.environ.get("FRONTEND_PORT", 8080)
print(f"Used frontend port: {FRONTEND_PORT}")

CORS_ORIGIN_WHITELIST = (
    f'http://localhost:{FRONTEND_PORT}',
    f'http://127.0.0.1:{FRONTEND_PORT}',
    f'http://{CURRENT_IP}:{FRONTEND_PORT}',
    f'http://hemera4.inf-cv.uni-jena.de:{FRONTEND_PORT}',
)

CSRF_TRUSTED_ORIGINS = (
    'https://api.inf-cv.uni-jena.de',
    'https://annot8.dikorsch.de',
    'http://localhost:8082',
)

CORS_ALLOW_HEADERS = list(default_headers) + [
    'contenttype',
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
