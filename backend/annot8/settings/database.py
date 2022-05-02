from annot8.settings.base import BASE_DIR

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': str(BASE_DIR / 'mysql.cnf'),
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",

        },
        'TEST': {
            "NAME": "annot8_tests"
        }
    }
}

