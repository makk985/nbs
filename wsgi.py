import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings') # Replace with your settings module
application = get_wsgi_application()