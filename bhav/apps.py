from django.apps import AppConfig
from . import scheduler

class BhavConfig(AppConfig):
    name = 'bhav'

    def ready(self):        
        print("Starting schedular...")
        scheduler.start()
