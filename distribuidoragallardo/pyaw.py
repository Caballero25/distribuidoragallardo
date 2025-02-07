dp = True

if dp:
    DB = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'distribuidoragallardo',
                'USER': 'postgres',
                'PASSWORD': '5862',
                'HOST': 'localhost',
                'PORT': '5432',
                'CONN_MAX_AGE': 600,
                'ATOMIC_REQUESTS': True
            }
        }