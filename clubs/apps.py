from django.apps import AppConfig


class ClubsConfig(AppConfig):
    name = 'clubs'

    def ready(self):
        import clubs.signals
