DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_project_db',
        'USER': 'postgres_user',
        'PASSWORD': 'supersecretpassword',
        'HOST': 'localhost', # Or your cloud database URL
        'PORT': '5432',
    }
}