from django.apps import AppConfig


class PapersConfig(AppConfig):
    name = 'papers'

    def ready(self):
        import papers.signals
    
