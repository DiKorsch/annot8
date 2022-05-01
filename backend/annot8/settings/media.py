import os
from pathlib import Path

from annot8.settings.base import BASE_DIR

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


MEDIA_ROOT = Path(os.environ.get("ANNOT8_MEDIA_ROOT", BASE_DIR / "media"))
STATIC_ROOT = Path(os.environ.get("ANNOT8_STATIC_ROOT", BASE_DIR / "static"))

STATICFILES_DIRS = [
]


PROJECTS_DIR = Path(os.environ.get("ANNOT8_PROJECTS_DIR", MEDIA_ROOT / "projects"))
